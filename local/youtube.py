from extraction import Extract
import pathlib as path
import asyncio
import subprocess
import json

class Youtube(Extract):
    #private
    async def __download_json(self, url) -> tuple[str, str]: #title description
        cmd = [
            "yt-dlp",
            "-J",
            str(url)
        ]

        proc_json = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout,stderr = await proc_json.communicate()

        data = json.loads(stdout.decode())

        title = data["title"]
        description = data["description"]

        return title, description

    async def __download_video(self, url) -> str: #path
        cmd = [
            "yt-dlp",
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
        

    async def __download(self, url) -> tuple[str, str, str]: #path, title, description

        (title, description), path = await asyncio.gather(
            self.__download_json(url),
            self.__download_video(url)
        )

        return path, title, description


    #protected
    def _extract(self):
        video_path, title, description = asyncio.run(self.__download(self.url))

        text = f"# {title}\n{description}"

        self._append_download(video_path)
        self._set_text(text)
    #public
