from extraction import Extract
import asyncio

class Youtube(Extract):
    #private
    def __download(url) -> tuple[str, str, str]: #path, title, description
        pass
    #protected
    def _extract(self):
        video, title, description = self.__download(self.url)

        text = f"# {title}\n{description}"

        self._append_download(video)
        self._set_text(text)
    #public
