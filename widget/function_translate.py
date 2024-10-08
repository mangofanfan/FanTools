import json, requests, hashlib, random, time
import sys
import traceback
from pathlib import Path
from urllib.parse import quote
import logging

import urllib3
from PySide2.QtGui import QIcon
from typing import List

from PySide2.QtWidgets import QWidget

logger = logging.getLogger("FanTools.funcT")

from widget.function import basicFunc, PIC
from widget.function_setting import cfg, qconfig
from widget.function_message import TranslateIB as IB


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

    SuffixList = [JSON]

class TranslateText:
    def __init__(self, originalText: str = None, translatedText: str = None, translateTag: str = None, id: int = None):
        self.originalText: str = originalText
        self.translatedText: str = translatedText
        self.translateTag: str = translateTag
        self.id: int = id

    def print(self):
        return f"{self.originalText}|!|{self.translatedText}|!|{self.translateTag}"

    def set(self, translatedText: str = None, translateTag: str = None):
        """
        用来标准化设置一个词条的翻译结果的方法。
        :param translatedText: 翻译目标文本。
        :param translateTag: 词条的翻译标签。
        :return: None
        """
        if translatedText != "" and translatedText is not None:
            self.translatedText = translatedText
        else:
            self.translatedText = "None"
        if self.translateTag == "None" or self.translateTag is None:
            self.translateTag = f";{translateTag}"
        elif translateTag in self.translateTag:
            pass
        else:
            self.translateTag += f";{translateTag}"
        return None


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
        :param file: 文件保存路径，默认为绝对路径。
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
            basicFunc.saveFile(file, temp, True)
        else:
            raise
        logger.info(f"已经将翻译项目成功导出至 {file}。")
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

    # 处理调用错误

    error_code = res.get("error_code")
    error_msg = res.get("error_msg")
    if error_code is not None and error_msg is not None:
        logger.error(f"百度翻译API调用错误，错误信息如下：{error_code} | {error_msg}")
        return None

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

    # 处理调用错误
    try:
        error_code = res.get("errorCode")
        if error_code == 0:
            raise
        logger.error(f"有道翻译API调用错误，错误代码：{error_code} | 请参阅有道提供的文档 [ https://ai.youdao.com/DOCSIRMA/html/trans/api/wbfy/index.html#section-10 ] 查看详情。")
        return None
    except Exception:
        pass

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
    def __init__(self, projectFile: str, file: str = None, preload: bool = True):
        """
        术语表对象。
        :param projectFile: 翻译项目工程文件路径，ft-translateProject.txt，str
        :param file: 术语表存储文件路径，ft-translateGlossary.txt，可选，str
        :param preload: 是否预先从路径加载文件。在调用目的为保存术语表时，必须指定为False。
        """
        self.projectFile = projectFile
        self.file = file
        if not self.file:
            self.file = self.projectFile.replace("ft-translateProject.txt", "ft-translateGlossary.txt")
        self.logger = logging.getLogger("FanTools.GlossaryTable")
        if preload:
            self.load()
        else:
            self.lineList = []

    def load(self, file: str = None):
        self.lineList = []
        if file is not None:
            self.file = file
        if not self.file:
            self.file = self.projectFile.replace("ft-translateProject.txt", "ft-translateGlossary.txt")

        # 在术语表文件尚不存在时新建术语表文件。
        try:
            data = basicFunc.readFile(self.file, True).split("\n")
        except FileNotFoundError:
            basicFunc.saveFile(self.file, "", True)
            data = basicFunc.readFile(self.file, True).split("\n")

        for line in data:
            if line != "" and line is not None:
                self.lineList.append(line.split("|!|"))

        self.logger.debug(f"成功加载 {self.projectFile} 的术语表于 {self.file} 。")
        return None

    def save(self, file: str = None):
        if file:
            self.file = file
        if not self.file:
            raise
        lineList = []
        _temp = []
        print(self.lineList)
        for line in self.lineList:
            if line not in _temp:
                _temp.append(line)
            else:
                self.logger.warning("保存术语表时发现重复词条，这可能是程序存在错误？")
                self.logger.warning("已跳过重复词条。")
                continue
            text = f"{line[0]}|!|{line[1]}|!|{line[2]}"
            lineList.append(text)
        fileText = "\n".join(lineList)
        basicFunc.saveFile(self.file, fileText, True)
        self.logger.debug(f"成功保存 {self.projectFile} 的术语表至 {self.file} 。")
        return None

    def add(self, originalText: str, targetText: str, middleTexts: list = None):
        if not middleTexts:
            middleTexts = "None"
        else:
            middleTexts = ";;".join(middleTexts)
        self.lineList.append([originalText, targetText, middleTexts])
        self.logger.debug(f"成功在术语表中添加字段 {originalText} ==>> {targetText} 。")
        return None

    def setMiddleTexts(self, originalText: str, middleTexts: list):
        """
        为术语表中的词条设置API翻译中间词。
        :param originalText: 术语表词汇原文。
        :param middleTexts: 中间词。
        :return: None
        """
        if len(middleTexts) == 1:
            middleTexts = middleTexts[0]
        else:
            middleTexts = ";;".join(middleTexts)
        for line in self.lineList:
            if originalText == line[0]:
                if len(line) == 2:
                    line.append(middleTexts)
                else:
                    line[2] = middleTexts
                self.logger.debug(f"成功为术语表字段 {originalText} 添加中间字段 {middleTexts} 。")
                self.save()
                return None
        self.logger.warning(f"未能在术语表中查找到词条 {originalText} 。")
        return None

    def addMiddleTexts(self, originalText: str, middleTexts: list):
        """
        为术语表中的词条添加API翻译中间词，如果尚不存在中间词则执行setMiddleTexts()。
        :param originalText: 术语表词汇原文。
        :param middleTexts: 中间词。
        :return: None
        """
        oldMiddleTexts: str = None
        for line in self.lineList:
            if originalText == line[0]:
                if len(line) == 3 and line[2] != "None":
                    oldMiddleTexts = line[2]
                else:
                    self.setMiddleTexts(originalText, middleTexts)
                    return None
                break
        if oldMiddleTexts is None:
            self.logger.warning(f"未能在术语表中查找到词条 {originalText} 。")
            return None

        middleTexts = ";;".join(oldMiddleTexts.split(";;") + middleTexts)
        line[2] = middleTexts
        self.save()
        return None

    def get(self, text: str) -> List[List[str]]:
        """
        对传入文本text，在术语表中匹配其中出现的术语。
        :param text: 传入文本（str）
        :return: 如果匹配成功，返回List[List[str]]结构的列表嵌套；如果匹配失败则返回None
        """
        _list = []
        for line in self.lineList:
            n = text.find(line[0])
            if n != -1:
                self.logger.debug(f"在术语表中查找到对应术语：{line[0]} ==>> {line[1]} (位置：{n})")
                _list.append(line)
        if not _list:
            self.logger.debug(f"查找术语表，但并未找到 {text} 中存在的术语。")
            return None
        else:
            self.logger.debug(f"已经返回文本 {text} 在术语表中的查询结果。")
            return _list

    def replace(self, text: str, _list: List[List[str]]):
        _text = text
        for line in _list:
            _text = _text.replace(line[0], line[1])
        self.logger.debug(f"术语表执行替换：{text} ==>> {_text}")
        return _text

    def remove(self, originalText: str):
        for line in self.lineList:
            if line[0] == originalText:
                self.lineList.remove(line)
                self.logger.debug(f"成功从术语表中移除字段 {originalText} 。")
                return None
        self.logger.error(f"未在术语表中查找到需要删除的字段 {originalText} 。")
        return None


class History:
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


def translate(originalText: str, apiFunc: staticmethod, self: QWidget, glossaryTable: GlossaryTable = None):
    try:
        targetText = apiFunc(originalText)
    except Exception as e:
        eType = sys.exc_info()[0]
        if eType == urllib3.exceptions.SSLError or eType == urllib3.exceptions.ProxyError or eType == requests.exceptions.ProxyError:
            logger.error("调用翻译接口的过程中出现SSL连接错误，请尝试启动工具箱设置中的「代理」配置，或关闭网络代理工具。")
            logger.error("此错误是Python网络库requests的错误（或者说不完善），与工具箱无关，我们无法从源头修复。")
            IB.msgSSLError(self)
            return None
        elif eType == urllib3.exceptions.ConnectTimeoutError:
            logger.error("调用翻译接口时出现连接超时问题，请检查网络连接状态与网络设置。")
            IB.msgTimeoutError(self)
            return None
        else:
            logger.error("调用翻译接口时出现奇怪的错误，请考虑将此错误提交！ | " + str(e))
            self.logger.error(traceback.format_exc())
            IB.msgOtherError(self)
            return None
    if targetText is None:
        logger.error("API返回参数错误，调用失败，这不是芒果工具箱所导致的问题。")
        IB.msgAPIError(self)
        return None

    # 术语表处理
    if glossaryTable is None:
        self.logger.debug("术语表翻译未启用，翻译结束。")
        return targetText
    lineList = glossaryTable.get(originalText)
    if lineList is None:
        self.logger.debug("术语表未匹配到符合词条，翻译结束。")
        return targetText
    self.logger.debug(f"针对 {originalText} 的API翻译检测到 {len(lineList)} 个术语表词条。")
    return [targetText, lineList]

