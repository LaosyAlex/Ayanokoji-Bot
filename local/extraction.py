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

    text = []
    attachments = []

    #protected
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
        for address in self.attachments:
            if os.path.exists(address):
                os.remove(address)

    @abstractmethod
    def extract(self):
        pass

    def compress(self):
        compression.text(self.text)

        for index, address in self.attachments:
            format = utils.fileType(address)

            match format:
                case "image":
                    self.attachments[index] = compression.image(address)
                case "video":
                    self.attachments[index] = compression.video(address)
                case "gif":
                    self.attachments[index] = compression.gif(address)
                case _:
                    print("Unknown file type")

    