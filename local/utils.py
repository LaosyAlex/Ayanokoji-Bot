import re

MAX_BYTES = 19 * (1024 ** 2)

__imageTypes = ["jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "svg", "ico", "heic", "heif", "avif"]
__gifTypes = ["gif"]
__videoTypes = ["mp4", "mkv", "mov", "avi", "webm", "flv", "wmv", "m4v", "mpeg", "mpg", "3gp", "ts", "mts", "m2ts"]

def fileType(address: str) -> str:
    format = re.split(r'\.', address)[-1]

    if format in __imageTypes:
        return "image"
    elif format in __videoTypes:
        return "video"
    elif format in __gifTypes:
        return "gif"
    else:
        return "unknown"

def get_link(text: str) -> str:
    start = text.find("https://")
    end = text.find(" ", start)

    if start != -1:
        if end == -1:  
            end = len(text)
        text = text[start:end]

    return text

gif_domains = {
    "tenor.com",
    "giphy.com",
    "klipy.com",
    "gifer.com",
    "gifdb.com",
    "makeagif.com",
    "imgur.com",
    "imgflip.com",
}