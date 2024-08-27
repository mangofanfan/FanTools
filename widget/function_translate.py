import json, requests, hashlib, random, time
from pathlib import Path
from urllib.parse import quote
import logging

from PySide2.QtGui import QIcon

logger = logging.getLogger("FanTools.funcT")

try:
    from function import basicFunc, PIC
    from function_setting import cfg, qconfig
except ModuleNotFoundError:
    from widget.function import basicFunc, PIC
    from widget.function_setting import cfg, qconfig


class TranslateTag:
    use_API = "使用API翻译"
    human = "人工翻译"
    repeat = "重复词条复制"


def readJson(file: str):
    with open(file, mode="r") as f:
        data: dict = json.load(f)
    return list(data.values())


class FileType:

    class Suffix:
        def __init__(self, name: str, readFunc: staticmethod):
            self.name = name.lower()
            self.readFunc = readFunc

    @staticmethod
    def checkFileType(fileType: Suffix, filePath: str):
        path = Path(filePath)
        if path.suffix != fileType.name:
            return False
        else:
            return True

    JSON = Suffix("json", readJson)

class TranslateText:
    def __init__(self, originalText: str = None, translatedText: str = None, translateTag: str = None, id: int = None):
        self.originalText: str = originalText
        self.translatedText: str = translatedText
        self.translateTag: str = translateTag
        self.id: int = id

    def print(self):
        return f"{self.originalText}|!|{self.translatedText}|!|{self.translateTag}"


class TranslateProject:
    """
    翻译项目类
    """
    def __init__(self):
        self.textList = []
        self.n = 0
        self.projectFile = None
        self.name = None

    def startProject(self, fileType: FileType.Suffix, file: str, name: str):
        """
        创建一个新的翻译工程项目。
        :param fileType:
        :param file: 源语言文件路径。
        :param name: 翻译工程文件的保存名前缀。
        :return:
        """
        if self.textList:
            logger.error("将要启动的 TranslateProject 中已经存在数据。")
            raise  # 如果已经有翻译数据则直接报错
        result: list = fileType.readFunc(file)
        n = 0
        for text in result:
            text: str
            n += 1
            item = TranslateText(originalText=text, id=n)
            self.textList.append(item)
        logger.info(f"启动了一个包含 {n} 个词条的翻译项目。（模式为 {fileType.name} | 待翻译文件路径为 {file}）")
        self.n = n

        backupFile = basicFunc.getHerePath() + f"/file/{name}.ft-originalFile.{fileType.name}"
        basicFunc.saveFile(backupFile, basicFunc.readFile(file, True), True)

        self.projectFile = basicFunc.getHerePath() + f"/file/{name}.ft-translateProject.txt"
        self.saveProject()

        logger.debug(f"已经保存原语言文件的备份至程序目录：{backupFile}")
        return None

    def loadProject(self, projectFile: str = None):
        """
        根据项目工程文件加载项目。
        :param projectFile: 项目工程文件路径。
        :return: None
        """
        if not self.projectFile:
            self.projectFile = projectFile
        tempList = basicFunc.readFile(self.projectFile, True).split("\n")
        n = 0
        for item in tempList:
            n += 1
            t = TranslateText(item.split("|!|")[0],
                              item.split("|!|")[1],
                              item.split("|!|")[2])
            t.id = n
            self.textList.append(t)
        logger.info(f"加载了一个包含 {n} 个词条的翻译项目。（工程文件路径为 {self.projectFile}）")
        self.n = n
        return None

    def saveProject(self, projectFile: str = None):
        if not self.projectFile:
            self.projectFile = projectFile
        tempList = []
        n = 0
        for text in self.textList:
            n += 1
            text: TranslateText
            tempList.append(text.print())
        temp = "\n".join(tempList)
        basicFunc.saveFile(self.projectFile, temp, True)
        logger.info(f"保存了一个包含 {n} 个词条的翻译项目。（工程文件路径为{self.projectFile}）")
        self.n = n
        return None

    def dumpProject(self, fileType: FileType.Suffix, file: str):
        """
        将已完成翻译的项目导出为正式的翻译语言文件。
        :param fileType:
        :param file: 文件保存路径
        :return: None
        """
        self.projectFile: str
        if fileType == FileType.JSON:
            result = {}
            for text in self.textList:
                text: TranslateText
                if text.translatedText != "None":
                    result[text.originalText] = text.translatedText
                else:
                    result[text.originalText] = ""
            with open(file=self.projectFile.replace("ft-translateProject.txt", f"ft-originalFile.{fileType.name}"), mode="r") as f:
                data: dict = json.load(f)
            for i in data.keys():
                for r in result.keys():
                    if data[i] == r:
                        data[i] = result[r]
            temp = json.dumps(data, ensure_ascii=False, indent=4)
            basicFunc.saveFile(file, temp)
            return None


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

    logger.debug(f"正在调用百度通用文本翻译API执行翻译，目标URL为 {fanyi_url} | 代理设置为 {proxies}")

    res: dict = requests.get(url=fanyi_url, proxies=proxies, timeout=3).json()

    trans_result: dict = res.get("trans_result")[0]
    targetText = trans_result["dst"]

    logger.debug(f"翻译结果：{originalText} ==>> {targetText}")

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

    logger.debug(f"正在调用有道文本翻译API执行翻译，目标URL为 {fanyi_url} | 代理设置为 {proxies}")

    res: dict = requests.get(url=fanyi_url, proxies=proxies, timeout=3).json()

    targetText = res["translation"][0]

    logger.debug(f"翻译结果：{originalText} ==>> {targetText}")

    return targetText


class TranslateAPI:

    class Api:
        def __init__(self, name: str, displayName: str, icon: str, apiFunc: staticmethod):
            self.name = name.lower()
            self.displayName = displayName
            self.icon = QIcon(icon)
            self.apiFunc = apiFunc

        def __str__(self):
            return self.name

        def apiFunc(self):
            return self.apiFunc

    BaiDu = Api(name="BaiDu", displayName="百度通用文本翻译API", icon=PIC.IconBaiDu, apiFunc=fanyi_baidu)
    YouDao = Api(name="YouDao", displayName="有道文本翻译API", icon=PIC.IconYouDao, apiFunc=fanyi_youdao)

    apiList = [BaiDu, YouDao]

    def get(self, name: str = None, displayName: str = None):
        """
        只需要提供 name 或 displayName 两个参数中的一个即可，然后将返回对应的Api对象。
        :param name:二选一即可，此项优先。
        :param displayName:二选一即可。
        :return:返回Api对象（TranslateAPI.Api）
        """
        name = name.lower()
        if name:
            for api in self.apiList:
                if api.name == name:
                    return api
        else:
            for api in self.apiList:
                if api.displayName == displayName:
                    return api


class GlossaryTable:
    def __init__(self, projectFile: str, file: str = None):
        self.projectFile = projectFile
        self.file = file
        if not self.file:
            p = Path(self.projectFile)
            self.file = p.parent.as_posix() + "/" + p.stem + ".txt"
        self.logger = logging.getLogger("FanTools.GlossaryTable")
        self.lineList = []

    def load(self, file: str = None):
        self.file = file
        self.lineList = []
        if not self.file:
            return None
        data = basicFunc.readFile(file, True).split("\n")
        for line in data:
            self.lineList.append(line.split("|!|"))

        self.logger.debug(f"成功加载 {self.projectFile} 的术语表于 {self.file} 。")
        return None

    def save(self, file: str = None):
        if file:
            self.file = file
        if not self.file:
            raise
        lineList = []
        for line in self.lineList:
            text = f"{line[0]}|!|{line[1]}"
            lineList.append(text)
        fileText = "\n".join(lineList)
        basicFunc.saveFile(self.file, fileText, True)
        self.logger.debug(f"成功保存 {self.projectFile} 的术语表至 {self.file} 。")
        return None

    def add(self, originalText: str, targetText: str):
        self.lineList.append([originalText, targetText])
        self.logger.debug(f"成功在术语表中添加字段 {originalText} ==>> {targetText} 。")
        return None

    def remove(self, originalText: str):
        for line in self.lineList:
            if line[0] == originalText:
                self.lineList.remove(line)
                return None
        self.logger.error(f"未在术语表中查找到需要删除的字段 {originalText} 。")


class history:
    def __init__(self):
        self.historyList = []
        self.logger = logging.getLogger("FanTools.TranslateHistory")
        self.path = basicFunc.getHerePath() + "/config/ft-translateHistory.txt"
        self.load()

    def load(self):
        if not Path(self.path).exists():
            f = open(file=self.path, mode="w")
            f.close()
            return
        with open(file=self.path, mode="r") as f:
            self.historyList = f.readlines()
        return None

    def add(self, path: str, name: str = None):
        for i in self.get():
            if path == i[0]:
                return None
        if not name:
            name = Path(path).stem
            name = name.split(".")[0]
        self.historyList.insert(0, f"{path}|!|{name}")
        self.save()
        return None

    def get(self):
            _list = []
            for i in self.historyList:
                i: str
                _list.append([i.split("|!|")[0], i.split("|!|")[1]])
            return _list

    def save(self):
        with open(file=self.path, mode="w") as f:
            f.write("\n".join(self.historyList))
        return None

    def clear(self):
        self.historyList.clear()
        self.save()
        return None
