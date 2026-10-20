#Need to add/finish error handling
#Also make more efficient

from PIL import Image
import os
from utils import MAX_BYTES
from pathlib import Path
import asyncio
import subprocess
import json
import re

def compress(infile):
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