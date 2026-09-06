from abc import ABC, abstractmethod
from enum import Enum
import os
import compression
import utils

class Extract:
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
    @property
    @abstractmethod
    def _website(self):
        pass

    @abstractmethod
    def _find_type():
        pass

    def _get_type(self):
        self.type

    def _append_download(self, path):
        self.__downloads.append(path)

    @abstractmethod
    def _extract(self):
        pass

    #public
    def __init__(self, url):
        self.url = url
        self.type = self._find_type()

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
    