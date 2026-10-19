from extraction import Extract
import subprocess
import json

class Generic(Extract):
    #Private
    @staticmethod
    def __get_json(url: str) -> dict | list | None:
        try:
            try:
                data = Generic._get_json_gallery_dl(url)
                return data
            except Exception as e1:
                print(type(e1).__name__, e1)
                try:
                    data = Generic._get_json_yt_dlp(url)
                    return data
                except Exception as e2:
                    raise ExceptionGroup(
                        "Both gallery-dl and yt-dlp failed to extract json.",
                        [e1, e2]
                    )
        except ExceptionGroup as e:
            print(e.message + "\n")

            for error in e.exceptions:
                if isinstance(error, subprocess.CalledProcessError):
                    print(f"{error.cmd[0]} failed:")
                    print(error.stderr)
                else:
                    print(type(error).__name__, error)

            return None

    @staticmethod
    def __get_info(data: dict | list) -> tuple[str, str]:
        title = Generic._find_field("title", data) or Generic._find_field("Title", data) or ""
        desc = Generic._find_field("description", data) or Generic._find_field("Description", data) or ""

        return title, desc

    def __download(self, url) -> list[any]:
        pass

    def __format_text(self, title, desc) -> str:
        pass

    #Protected
    def _extract(self):
        pass

    #Public
    def test(self):
        self.__get_json(self.url)