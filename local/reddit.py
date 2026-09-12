from extraction import Extract

class Reddit(Extract):
    #private
    def __json_url(url) -> str: #return url.json
        pass

    def __retrieve_reddit_json(json_url) -> str: #return json as string
        pass

    def __reddit_download(json_str) -> list[any]: #return list of paths
        pass

    def __reddit_text(json_str) -> str: #return f"# {title}\n{description}""
        pass 

    #protected
    def _extract(self):
        __json_url = self.__json_url(self.url)
        __json_str = self.__retrieve_reddit_json(__json_url)

        __paths = self.__reddit_download(__json_str) 
        for path in __paths:
            self._append_download(path)

        __text = self.__reddit_text(__json_str)
        self._set_text(__text)
         
    #public

