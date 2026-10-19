from extraction import Extract
import subprocess
import json
import asyncio
from utils import __imageTypes as imageTypes


class Reddit(Extract):
    #private
    def __retrieve_reddit_json(self, url) -> dict: #return json dict
        cmd = [
            "gallery-dl",
            "-J",
            "--cookies-from-browser", "firefox",
            str(url)
        ]

        result = subprocess.run([*cmd], capture_output=True, text= True)

        data = json.loads(result.stdout.strip())

        post_dict = data[0][1]

        return post_dict

    def __post_type(self, post_dict) -> str:
        if post_dict.get("url").lower().endswith(".gif"):
            return "GIF"
        elif post_dict.get("is_video"):
            return "VIDEO"
        elif post_dict.get("is_self"):
            return "TEXT"
        elif post_dict.get("is_gallery"):
            return "GALLERY"
        elif post_dict.get("url").lower().endswith(tuple("." + ext for ext in imageTypes)):
            return "IMAGE"
        else:
            return "UNKNOWN"
        #do something for URLs/Youtube posts

    def __reddit_download(self, post_type, url) -> list[str]: #return list of paths
        paths = []

        match post_type:
            case "VIDEO" | "IMAGE" | "GIF":
                path = asyncio.run(self._download_single(url))
                paths.append(path)
            case "GALLERY":
                paths = asyncio.run(self._download_gallery(url))

        return paths


    def __reddit_text(self, post_dict) -> str: #return f"# {title}\n{description}""
        pass 

    #protected
    def _extract(self):
        __json_str = self.__retrieve_reddit_json(self.url)

        __paths = self.__reddit_download(__json_str) 
        self._append_download(__paths)

        __text = self.__reddit_text(__json_str)
        self._set_text(__text)
         
    #public
    def test(self):
        post_data = self.__retrieve_reddit_json(self.url)
        post_type = self.__post_type(post_data)
        paths = self.__reddit_download(post_type, self.url)

        for path in paths:
            print(f"{path}\n")

        print(post_type)
