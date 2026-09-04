import re

__imageTypes = ["jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "svg", "ico", "heic", "heif", "avif"]
__gifTypes = ["gif"]
__videoTypes = ["mp4", "mkv", "mov", "avi", "webm", "flv", "wmv", "m4v", "mpeg", "mpg", "3gp", "ts", "mts", "m2ts"]

def fileType(address):
    format = re.split('\.', address)[1]

    if format in __imageTypes:
        return "image"
    elif format in __videoTypes:
        return "video"
    elif format in __gifTypes:
        return "gif"
    else:
        return "unknown"

