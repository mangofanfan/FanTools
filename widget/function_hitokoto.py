import requests
import json
import logging

from PySide2.QtCore import QObject, QThread, Signal

from widget.function_setting import cfg

logger = logging.getLogger("FanTools.Hitokoto")


class yi_yan(QObject):
    GUIUpdateSignal = Signal(dict)

    def __init__(self):
        """
        需要在调用self.setApi()之后，self.api才能获得值。
        或直接调用get方法。
        """
        super().__init__()
        self.dict = {"official": "https://v1.hitokoto.cn/",
                      "hitokoto": "https://hitokoto.cn/",
                      "fan_mirror": "https://api-hitokoto.mangofanfan.cn/"}
        self.api: str = None
        self._name: str = None
        self.Thread_Timer = QThread()
        self.Worker_Timer = Worker_Timer()
        self.Worker_Timer.updateSignal.connect(self.get)
        self.Worker_Timer.moveToThread(self.Thread_Timer)
        self.Thread_Timer.start()

    def start(self):
        """
        启用一言循环，定时获取新的一言并通过信号发送到GUI。
        :return: None
        """
        self.Worker_Timer.runSignal.emit()
        logger.debug("已启动一言API更新的定时线程。")
        return None

    def setApi(self, name: str):
        """
        设置一言API的调用地址，设置之后self.api会获得值。
        无需手动调用，可以直接调用分装好的get方法。
        :param name: API名称，多个单词之间需要用下划线连接，所有字母不区分大小写。
        :return: None
        """
        self._name = name.lower()
        self.api = self.dict[self._name]
        return None

    def get(self):
        self.setApi(cfg.get(cfg.YiYanAPI))
        self.GUIUpdateSignal.emit(self._get())
        return None

    def _get(self):
        """
        （内部方法）获取一条新的一言，避免直接外部调用此方法。
        :return: None
        """
        if cfg.get(cfg.ProxyEnable):
            proxies = {
                'http': cfg.get(cfg.ProxyHttp),
                'https': cfg.get(cfg.ProxyHttps),
            }
        else:
            proxies = {}

        cfgItems = [cfg.YiYanTypeA, cfg.YiYanTypeB, cfg.YiYanTypeC, cfg.YiYanTypeD, cfg.YiYanTypeE, cfg.YiYanTypeF,
                    cfg.YiYanTypeG, cfg.YiYanTypeH, cfg.YiYanTypeI, cfg.YiYanTypeJ, cfg.YiYanTypeK, cfg.YiYanTypeL]
        types = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]

        n = 0
        i = 0
        typeList = []
        for cfgItem in cfgItems:
            if cfg.get(cfgItem) is True:
                n += 1
                typeList.append(types[i])
            i += 1

        if n == 0:
            _api = self.api
        elif n == 1:
            _api = self.api + "?c=" + typeList[0]
        elif n >= 2:
            _api = self.api + "?c=" + "&c=".join(typeList)
        else:
            raise

        logger.debug(f"调用一次一言 API： {_api}")
        res = requests.get(_api, proxies=proxies)
        data = json.loads(res.content)

        _from = data["from"]
        _from_who = data["from_who"]
        if _from_who != "null" and _from_who is not None and _from_who != "None":
            origin = f"{_from_who} - {_from}"
        else:
            origin = _from

        # 处理返回的数据
        result = {"content": data["hitokoto"],
                  "origin": origin,
                  "id": str(data["id"])}

        return result


class Worker_Timer(QObject):
    runSignal = Signal()
    updateSignal = Signal()

    def __init__(self):
        super().__init__()

        self.runSignal.connect(self.run)
        self.keepRunning = True

    def stopRunning(self):
        self.keepRunning = False
        return None

    def run(self):
        from time import sleep
        while self.keepRunning:
            self.updateSignal.emit()
            logger.debug("发送一次一言更新信号。")
            _time = cfg.get(cfg.TimeSleep)
            sleep(_time)


