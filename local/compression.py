from PIL import Image
import os
from utils import MAX_BYTES
from pathlib import Path
import asyncio
import subprocess
import json

def __video_Compression_Calc(bitrate, width, height, FPS):
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



def video(infile):
    if os.path.getsize(infile) < MAX_BYTES:
        return infile
    else:
        outfile = Path(infile).with_stem(Path(infile).stem + "_compressed")


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