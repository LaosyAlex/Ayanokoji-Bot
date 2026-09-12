from PIL import Image
import os
from utils import MAX_BYTES
from pathlib import Path
import asyncio
import subprocess
import json
import re

def __video_Compression_Calc(total_bitrate, width, height, FPS) -> tuple[float, float, int, float]:
    #return audio_bitrate, video_bitrate, height, FPS
    
    #audio: 256k, 128k, 64k, 32k, 16k, 8k....

    #Formula BPPPPF = video_bitrate / (width * height * FPS)

    audio_bitrate = total_bitrate * 0.12 #change this to bitrarte brackets with floor 16k
    video_bitrate = total_bitrate - audio_bitrate

    new_FPS = FPS

    while True:
        BPPPF = video_bitrate / (width * height * new_FPS)

        if BPPPF > 0.08:
            return audio_bitrate, video_bitrate, height, new_FPS
        elif new_FPS < 5:
            width //= 2
            width -= width % 2
            height //= 2
            height -= height % 2
            new_FPS = FPS
        else:
            new_FPS -= 1

async def __get_video_info(path):
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

async def __compress_video(infile, outfile, audio_bitrate, video_bitrate, height, FPS):
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

def video(infile):
    if os.path.getsize(infile) < MAX_BYTES:
        return infile
    else:
        outfile = Path(infile).with_stem(Path(infile).stem + "_compressed").with_suffix(".mp4")

        duration, width, height, FPS = asyncio.run(__get_video_info(infile))
        total_bitrate = MAX_BYTES * 8 / duration

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

async def __gif_info(infile):
    cmd = [
        "gifsicle",
        "--info",
        str(infile),
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    info = stdout.decode()
    match = re.search(r"logical screen \d+x(?P<height>\d+).*global color table \[(?P<palette>\d+)\]", info, re.DOTALL)

    height = int(match.group("height"))
    palette = int(match.group("palette"))

    return height, palette


async def __compress_gif(infile):
    outfile = Path(infile).with_stem(Path(infile).stem + "_compressed")

    for i in range(1, 4):
        print(i)

        cmd = [
            "gifsicle",
            f"-O{i}",
            "-k", "256",
            str(infile),
            "-o", str(outfile),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

        _, stderr = await proc.communicate()

        if os.path.getsize(outfile) < MAX_BYTES:
            return outfile
    else:
        height, k_original = asyncio.run(__gif_info(infile))
        lossy = 40
        if k_original > 256:
            k_original = 256
        else:
            k = k_original

        i = 0

        while True:
            i += 1
            print(i)
            cmd = [
                "gifsicle",
                f"-O{i}",
                "-k", k,
                "--lossy", lossy,
                "--resize", "_x{height}",
                str(infile),
                "-o", str(outfile)
            ]

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE
            )

            _,stderr = await proc.communicate()

            if os.path.getsize(outfile) < MAX_BYTES:
                return outfile
            elif lossy > 120:
                lossy = 20
                k /= 2
            elif k < 64:
                lossy = 20
                k = k_original
                height /= 2

                

def gif(infile):
    if os.path.getsize(infile) < MAX_BYTES:
        return infile
    else:
        outfile = asyncio.run(__compress_gif(infile))
        return outfile


def text(textList):
    text = textList[0]
    textList.clear()

    while len(text) > 1900:
        textList.append(text[0:1900])
        text = text[1900:] + "..."

    textList.append(text)