from PIL import Image
import os
from utils import MAX_BYTES
from pathlib import Path
import asyncio
import subprocess
import json
import re

def compress(textList: list) -> None:
    try:
        text = textList[0]
        textList.clear()

        while len(text) > 1900:
            textList.append(text[0:1900])
            text = text[1900:] + "..."

        textList.append(text)
    except Exception as error:
        error.add_note("Text compression failed.")
        raise