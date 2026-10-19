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
        desc = Generic._find_field("description", data) or Generic._find_field("Description", data) or Generic._find_field("selftext", data) or ""

        return title, desc

    @staticmethod
    def __download(url: str) -> list[any] | str:
        try:
            try:
                paths = Generic._download_gallery_dl(url)
                return paths
            except Exception as e1:
                print(type(e1).__name__, e1)
                try:
                    paths = Generic._download_yt_dlp(url)
                    return paths
                except Exception as e2:
                    raise ExceptionGroup(
                        "Both gallery-dl and yt-dlp failed to download.",
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
    def __format_text(title: str, desc: str) -> str:
        text = (title + "\n\n" if title else "") + desc

        return text or ""

    #Protected
    def _extract(self):
        __data = Generic.__get_json(self.url)
        __title, __desc = Generic.__get_info(__data)
        __text = Generic.__format_text(__title, __desc)
        self._set_text(__text)
        print(__text)

        __paths = Generic.__download(self.url) or ""
        self._append_download(__paths)

        print("PATHS: \n\n")
        if isinstance(__paths, list):
            for path in __paths:
                print(path)
        else:
            print(__paths)

    #Public
