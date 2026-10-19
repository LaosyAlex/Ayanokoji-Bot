from extraction import Extract
import subprocess
import json

class Generic(Extract):
    #Private
    def __get_json(self, url) -> dict:
        try:
            try:
                cmd = [
                    "gallery-dl",
                    "-j",
                    "--cookies-from-browser", "firefox",
                    str(url)
                ]

                result = subprocess.run([*cmd], capture_output=True, text= True, check=True)

                data = json.loads(result.stdout.strip())

                if not data:
                    raise ValueError("gallery-dl returned empty JSON")
                
                print(f"gallery-dl:\n\n{data}")
                return data
            except Exception as e1:
                try:
                    print(type(e1).__name__, e1)

                    cmd = [
                        "yt-dlp",
                        "-J",
                        "--cookies-from-browser", "firefox",
                        "--ignore-no-formats-error",
                        str(url)
                    ]

                    result = subprocess.run([*cmd], capture_output=True, text= True, check=True)

                    data = json.loads(result.stdout.strip())

                    if not data:
                        raise ValueError("yt-dlp returned empty JSON")
                    
                    print(f"yt-dlp:\n\n{data}")
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

    def __get_info(self, json) -> tuple[str, str]:
        pass

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