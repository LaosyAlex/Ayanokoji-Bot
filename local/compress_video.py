#Need to add/finish error handling

from PIL import Image
import os
from utils import MAX_BYTES
from pathlib import Path
import asyncio
import subprocess
import json

def __video_Compression_Calc(total_bitrate: int, width: int, height: int, FPS: int) -> tuple[float, float, int, float]:
    #return audio_bitrate, video_bitrate, height, FPS
    
    #audio: 256k, 128k, 64k, 32k, 16k (floor)

    #Formula BPPPPF = video_bitrate / (width * height * FPS)

    try:
        audio_bitrate = 256*1000
        video_bitrate = total_bitrate - audio_bitrate

        new_FPS = FPS

        while True:
            BPPPF = video_bitrate / (width * height * new_FPS)

            if BPPPF > 0.08:
                return audio_bitrate, video_bitrate, height, new_FPS
            elif new_FPS < 5:
                new_FPS = FPS

                if audio_bitrate > 16*1000:
                    video_bitrate += audio_bitrate
                    audio_bitrate /= 2
                    video_bitrate -= audio_bitrate
                else:
                    width //= 2
                    width -= width % 2
                    height //= 2
                    height -= height % 2
            else:
                new_FPS -= 1
    except Exception as error:
        print("Something went wrong while calculating video compression.")
        print(type(error).__name__, error)

async def __get_video_info(path: str) -> tuple[int, int, int, int]:
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "format=duration:stream=width,height,avg_frame_rate",
            "-of", "json",
            str(path)
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()
        data = json.loads(stdout.decode())

        duration = float(data["format"]["duration"])
        width = int(data["streams"][0]["width"])
        height = int(data["streams"][0]["height"])

        num, den = data["streams"][0]["avg_frame_rate"].split("/")
        FPS = int(num) / int(den)

        return duration, width, height, FPS
    except Exception as error:
        print("something went wrong while trying to extract video specs.")
        if isinstance(error, subprocess.CalledProcessError):
            print(f"{error.cmd[0]} failed:")
            print(error.stderr)
        else:
            print(type(error).__name__, error)

    

async def __compress_video(infile: str, outfile: str, audio_bitrate: int, video_bitrate: int, height: int, FPS: int):
    try:
        cmd = [
            "ffmpeg",
            "-y", 
            "-i", str(infile),
            "-vf", f"scale=-2:{height}",
            "-r", str(FPS),
            "-c:v", "libx264",
            "-b:v", str(video_bitrate),
            "-c:a", "aac",
            "-b:a", str(audio_bitrate),
            str(outfile)
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

        _, stderr = await proc.communicate() 

        print(stderr.decode())
    except Exception as error:
        print("Something went wrong while compressing the video.")
        if isinstance(error, subprocess.CalledProcessError):
            print(f"{error.cmd[0]} failed:")
            print(error.stderr)
        else:
            print(type(error).__name__, error)

def compress(infile):
    if os.path.getsize(infile) < MAX_BYTES:
        return infile
    else:
        outfile = Path(infile).with_stem(Path(infile).stem + "_compressed").with_suffix(".mp4")

        duration, width, height, FPS = asyncio.run(__get_video_info(infile))
        total_bitrate = MAX_BYTES * 8 / duration

        audio_bitrate, video_bitrate, height, FPS = __video_Compression_Calc(total_bitrate, width, height, FPS)
        asyncio.run(__compress_video(infile, outfile, audio_bitrate, video_bitrate, height, FPS))

        return outfile