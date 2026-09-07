from PIL import Image
import os
from utils import MAX_BYTES
from pathlib import Path
import asyncio
import subprocess
import json

def __video_Compression_Calc(total_bitrate, width, height, FPS) -> tuple[float, float, int, float]:
    pass

async def __get_video_info(path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "format=duration : stream=width,height,avg_frame_rate",
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

async def __compress_video(infile, outfile, audio_bitrate, video_bitrate, height, FPS):
    cmd = [
        "ffmpeg",
        "-y", 
        "-i", str(infile),
        "-vf", f"scale=-2:{height}",
        "-r", FPS,
        "-c:v", "libx264",
        "-b:v", video_bitrate,
        "-c:a", "aac",
        "-b:a", audio_bitrate,
        str(outfile)
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )

    _, stderr = await proc.communicate() 

def video(infile):
    if os.path.getsize(infile) < MAX_BYTES:
        return infile
    else:
        outfile = Path(infile).with_stem(Path(infile).stem + "_compressed")

        duration, width, height, FPS = asyncio.run(__get_video_info(infile))
        total_bitrate = MAX_BYTES

        audio_bitrate, video_bitrate, height, FPS = __video_Compression_Calc(total_bitrate, width, height, FPS)
        asyncio.run(__compress_video(infile, outfile, audio_bitrate, video_bitrate, height, FPS))




def image(infile):
    if os.path.getsize(infile) < MAX_BYTES:
        return infile
    else:
        with Image.open(infile) as original:
            width, height = original.size
            quality = 95

            outfile = Path(infile).with_stem(Path(infile).stem + "_compressed").with_suffix(".WEBP")

            while True:
                original.save(outfile, format="WEBP", quality=quality)

                if os.path.getsize(outfile) < MAX_BYTES:
                    return outfile
                elif quality < 25:
                    quality = 95
                    width //= 2
                    height //= 2

                    original = original.resize((width, height))
                else:
                    quality -= 5


def gif():
    pass

def text(textList):
    text = textList[0]
    textList.clear()

    while len(text) > 1900:
        textList.append(text[0:1900])
        text = text[1900:] + "..."

    textList.append(text)