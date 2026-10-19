from abc import ABC, abstractmethod
from enum import Enum
import os
import compression
import utils
import asyncio
import subprocess

class Extract(ABC):
    #private
    class __Type(Enum):
        UNKNOWN = 0
        VIDEO = 1
        IMAGE = 2
        GALLERY = 3

    __downloads = []

    __text = []
    __attachments = []

    def __compress(self):
        compression.text(self.__text)

        for path in self.__downloads:
            format = utils.fileType(path)

            match format:
                case "image":
                    self.__attachments.append(compression.image(path))
                case "video":
                    self.__attachments.append(compression.video(path))
                case "gif":
                    self.__attachments.append(compression.gif(path))
                case _:
                    print("Unknown file type")

    #protected
    '''
    @property
    @abstractmethod
    def _website(self):
        pass

    @abstractmethod
    def _find_type():
        pass

    def _get_type(self):
        self.type
    '''
    def _is_403(stderr: str) -> bool:
        if "403 forbidden" in stderr.lower():
            return True
        else:
            return False

    async def _download_video(self, url) -> str: #path
        cmd = [
            "gallery-dl",
            "--cookies-from-browser", "firefox",
            "-P", r"local\temp",
            "--print", "after_move:filepath",
            str(url)
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        path = stdout.decode()

        return str(path).strip()

    async def _download_single(self, url) -> str: #path
        cmd = [
            "gallery-dl",
            "--cookies-from-browser", "firefox",
            "-D", r"local\temp",
            str(url)
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        path = stdout.decode("cp1252")

        return str(path).removeprefix("# ").strip()

    async def _download_gallery(self, url) -> list[str]: #path
        cmd = [
            "gallery-dl",
            "--cookies-from-browser", "firefox",
            "-D", r"local\temp",
            str(url)
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        paths = stdout.decode("cp1252").splitlines()

        for index, path in enumerate(paths):
            paths[index] = str(path).removeprefix("# ").strip()

        return paths

    def _set_text(self, text):
        pass

    def _append_download(self, paths: str | list[str]):
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            self.__downloads.append(path)

    @abstractmethod
    def _extract(self):
        pass

    #public
    def __init__(self, url):
        self.url = url
        #self.type = self._find_type()

    def __del__(self):
        for path in self.__downloads:
            if os.path.exists(path):
                os.remove(path)

        for path in self.__attachments:
            if os.path.exists(path):
                os.remove(path)

    def process(self):
        self._extract()
        self.__compress()

        return self.__text, self.__attachments
    