import aria2p
from typing import List

from widget.function import basicFunc


class Manager:
    def __init__(self):
        self.aria2: aria2p.API

    def aria2_run(self):
        self.aria2 = aria2p.API(
            aria2p.Client(
                host = "http://localhost" ,
                port = 6800 ,
                secret = ""
            )
        )
        self.aria2.set_global_options({"dir": basicFunc.getHerePath() + "/file"})
        return None

    def aria2_exit(self):
        self.aria2.stop_listening()
        return None

    def getStatus(self):
        return self.aria2.get_stats()

    def addUrls(self, urls: List[str], path: str = None):
        if not path:
            return self.aria2.add_uris(urls)
        else:
            return self.aria2.add_uris(urls, {"dir": path})




