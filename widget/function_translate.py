import json, requests, hashlib, random, time
from urllib.parse import quote

try:
    from function import basicFunc
    from function_setting import cfg, qconfig
except:
    from widget.function import basicFunc
    from widget.function_setting import cfg, qconfig


class TranslateTag:
    use_API = "使用API翻译"
    human = "人工翻译"
    repeat = "重复词条复制"


class FileType:
    JSON = "json"


class TranslateText:
    def __init__(self, originalText: str = None, translatedText: str = None, translateTag: str = None, id: int = None):
        self.originalText: str = originalText
        self.translatedText: str = translatedText
        self.translateTag: str = translateTag
        self.id: int = id

    def print(self):
        return f"{self.originalText}|!|{self.translatedText}|!|{self.translateTag}"


class TranslateProject:
    def __init__(self):
        self.textList = []
        self.n = 0

    def startProject(self, mode: staticmethod, file: str):
        if self.textList:
            raise  # 如果已经有翻译数据则直接报错
        result: list = mode(file)
        n = 0
        for text in result:
            text: str
            n += 1
            item = TranslateText(originalText=text, id=n)
            self.textList.append(item)
        print(f"开始了一个包含 {n} 个词条的翻译项目。")
        self.n = n
        return None

    def loadProject(self, file: str):
        tempList = basicFunc.readFile(file, True).split("\n")
        n = 0
        for item in tempList:
            n += 1
            t = TranslateText(item.split("|!|")[0],
                              item.split("|!|")[1],
                              item.split("|!|")[2])
            t.id = n
            self.textList.append(t)
        print(f"加载了一个包含 {n} 个词条的翻译项目。")
        self.n = n
        return None

    def saveProject(self, file: str):
        tempList = []
        n = 0
        for text in self.textList:
            n += 1
            text: TranslateText
            tempList.append(text.print())
        temp = "\n".join(tempList)
        basicFunc.saveFile(file, temp, True)
        print(f"保存了一个包含 {n} 个词条的翻译项目。")
        self.n = n
        return None

    def dumpProject(self, fileType: FileType, file: str):
        if fileType == FileType.JSON:
            result = {}
            for text in self.textList:
                text: TranslateText
                if text.translatedText != "None":
                    result[text.originalText] = text.translatedText
                else:
                    result[text.originalText] = ""
            with open(r"C:\Users\mango\Downloads\Noxcrew-Terra_Swoop_Force_ResourcePack_v1.1.0_Java\en_us.json", "r") as f:
                data: dict = json.load(f)
            for i in data.keys():
                for r in result.keys():
                    if data[i] == r:
                        data[i] = result[r]
            temp = json.dumps(data, ensure_ascii=False)
            basicFunc.saveFile(file, temp)


def readJson(file: str):
    with open(file, mode="r") as f:
        data: dict = json.load(f)
    return list(data.values())


def fanyi_baidu(originalText: str, originalLan: str = "en", targetLan: str = "zh"):
    fanyi_api = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    appid = qconfig.get(cfg.BaiduAPPID)
    key = qconfig.get(cfg.BaiduKey)
    salt = str(random.randint(100000, 999999))
    sign = hashlib.md5((appid + originalText + salt + key).encode("utf-8")).hexdigest()

    fanyi_url = f"{fanyi_api}?q={quote(originalText)}&from={originalLan}&to={targetLan}&appid={appid}&salt={salt}&sign={sign}"

    if qconfig.get(cfg.ProxyEnable):
        proxies = {
            'http': qconfig.get(cfg.ProxyHttp),
            'https': qconfig.get(cfg.ProxyHttps),
        }
    else:
        proxies = {}

    res: dict = requests.get(url=fanyi_url, proxies=proxies, timeout=3).json()

    trans_result: dict = res.get("trans_result")[0]
    targetText = trans_result["dst"]

    return targetText


def fanyi_youdao(originalText: str, originalLan: str = "en", targetLan: str = "zh-CHS"):
    fanyi_api = "https://openapi.youdao.com/api"
    appKey = qconfig.get(cfg.YoudaoAPPKey)
    key = qconfig.get(cfg.YoudaoKey)
    utcTime = str(int(time.time()))
    salt = str(random.randint(100000, 999999))

    # 根据 originalText 的长度来决定签名格式
    if len(originalText) > 20:
        input_ = originalText[0:10] + str(len(originalText)) + originalText[-10:len(originalText)]
    else:
        input_ = originalText
    sign = hashlib.sha256((appKey + input_ + salt + utcTime + key).encode("utf-8")).hexdigest()

    fanyi_url = f"{fanyi_api}?q={quote(originalText)}&from={originalLan}&to={targetLan}&appKey={appKey}&salt={salt}&sign={sign}&signType=v3&curtime={utcTime}"

    if qconfig.get(cfg.ProxyEnable):
        proxies = {
            'http': qconfig.get(cfg.ProxyHttp),
            'https': qconfig.get(cfg.ProxyHttps),
        }
    else:
        proxies = {}

    res: dict = requests.get(url=fanyi_url, proxies=proxies, timeout=3).json()

    targetText = res["translation"][0]

    return targetText

