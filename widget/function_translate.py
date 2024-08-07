import json
import requests
import hashlib
import random

try:
    from function import basicFunc
except:
    from widget.function import basicFunc


class TranslateTag:
    use_API = "使用API翻译"
    human = "人工翻译"


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
        tempList = basicFunc.readFile(file).split("\n")
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
        basicFunc.saveFile(file, temp)
        print(f"保存了一个包含 {n} 个词条的翻译项目。")
        self.n = n
        return None


def readJson(file: str):
    with open(file, mode="r") as f:
        data: dict = json.load(f)
    return list(data.values())


def fanyi_baidu(originalText: str, originalLan: str = "en", targetLan: str = "zh"):
    fanyi_api = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    appid = "20220208001076927"
    key = "zwX78gFP3O4dA0Mwf7zD"
    salt = random.randint(100000, 999999)
    sign = hashlib.md5((appid + originalText + str(salt) + key).encode("utf-8")).hexdigest()

    fanyi_url = f"{fanyi_api}?q={originalText}&from={originalLan}&to={targetLan}&appid={appid}&salt={salt}&sign={sign}"

    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }

    res: dict = requests.get(url=fanyi_url, proxies=proxies, timeout=3).json()

    trans_result: dict = res.get("trans_result")[0]
    targetText = trans_result["dst"]

    return targetText

