from abc import ABC, abstractmethod
from enum import Enum
import os
import compression
import utils
import asyncio
import subprocess
import json

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
    @staticmethod
    def _find_field(field: str, data: dict | list) -> object | None:
        if isinstance(data, dict):
            for i, v in data.items():
                if i == field:
                    return v
                else:
                    if isinstance(v, (dict | list)):
                        result = Extract._find_field(field, v)
                        if result is not None:
                            return result
        elif isinstance(data, list):
            for v in data:
                if isinstance(v, (dict | list)):
                    result = Extract._find_field(field, v)
                    if result is not None:
                        return result
        
        return None

    @staticmethod
    def _is_403(stderr: str) -> bool:
        if "403 forbidden" in stderr.lower():
            return True
        else:
            return False

    @staticmethod
    def _get_json_gallery_dl(url: str) -> dict | list:
        cmd = [
            "gallery-dl",
            "-v",
            "-j",
            "--cookies-from-browser", "firefox",
            str(url)
        ]

        result = subprocess.run([*cmd], capture_output=True, text= True, check=False)

        data = json.loads(result.stdout.strip())

        if Extract._is_403(result.stderr):
            raise PermissionError("Request was blocked by site.")
        
        if not data:
            raise ValueError("gallery-dl returned empty JSON.")
        
        return data

    @staticmethod
    def _download_gallery_dl(url: str) -> list[str] | str:
        cmd = [
            "gallery-dl",
            "-v",
            "--cookies-from-browser", "firefox",
            "-D", r"local\temp",
            str(url)
        ]

        result = subprocess.run([*cmd], capture_output=True, text=True, check=False)

        if Extract._is_403(result.stderr):
            raise PermissionError("Request was blocked by site.")

        paths = result.stdout.splitlines()

        for index, path in enumerate(paths):
            paths[index] = str(path).removeprefix("# ").strip()

        return paths

    @staticmethod
    def _get_json_yt_dlp(url: str) -> dict | list:
        cmd = [
            "yt-dlp",
            "-v",
            "-J",
            "--cookies-from-browser", "firefox",
            "--ignore-no-formats-error",
            str(url)
        ]

        result = subprocess.run([*cmd], capture_output=True, text= True, check=False)

        data = json.loads(result.stdout.strip())

        if Extract._is_403(result.stderr):
            raise PermissionError("Request was blocked by site.")
        
        if not data:
            raise ValueError("yt-dlp returned empty JSON.")
        
        return data

    @staticmethod
    def _download_yt_dlp(url: str) -> list[str] | str:
        cmd = [
            "yt-dlp",
            "-v",
            "-P", r"local\temp",
            "--print", "after_move:filepath",
            "--cookies-from-browser", "firefox",
            str(url)
        ]

        result = subprocess.run([*cmd], capture_output=True, text=True, check=False)

        if Extract._is_403(result.stderr):
            raise PermissionError("Request was blocked by site.")

        path = result.stdout.decode()

        return str(path).strip()

    def _set_text(self, text):
        pass

    def _append_download(self, paths: str | list[str]) -> None:
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
    