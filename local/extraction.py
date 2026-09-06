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

    #public
    def __init__(self, url):
        self.url = url
        self.type = self._find_type()

    def __del__(self):
        for address in self.__downloads:
            if os.path.exists(address):
                os.remove(address)

        for address in self.__attachments:
            if os.path.exists(address):
                os.remove(address)

    @abstractmethod
    def extract(self):
        pass

    def compress(self):
        compression.text(self.__text)

        for address in self.__downloads:
            format = utils.fileType(address)

            match format:
                case "image":
                    self.__attachments.append(compression.image(address))
                case "video":
                    self.__attachments.append(compression.video(address))
                case "gif":
                    self.__attachments.append(compression.gif(address))
                case _:
                    print("Unknown file type")

    