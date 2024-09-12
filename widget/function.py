from os import getcwd, getenv
from pathlib import Path

from PySide2.QtWidgets import QFileDialog


class basicFunc:
    def __init__(self):
        pass

    @staticmethod
    def getInfo():
        info = {"v": "0.1.0",
                "a": "MangoFanFan_",
                "au": "https://mangofanfan.cn/",
                "github": "https://github.com/mangofanfan/FanTools",
                "docs": "https://docs.mangofanfan.cn/fantools/",
                "publish": "https://ifanspace.top/2024/08/27/498.html",
                "updateLog": "https://ifanspace.top/2024/08/28/510.html"}
        return info

    @staticmethod
    def getHerePath():
        if Path(getcwd() + "/data").is_dir():
            return getcwd()
        else:
            return getenv("LOCALAPPDATA") + "/FanTools"

    @staticmethod
    def readFile(file: str, realPath: bool = False) -> str:
        if realPath:
            with open(file=file, mode="r", encoding="utf-8") as f:
                r = f.read()
            return r
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="r", encoding="utf-8") as f:
            r = f.read()
        return r

    @staticmethod
    def saveFile(file: str, text: str, realPath: bool = False):
        path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        if realPath:
            with open(file=file, mode="w+", encoding="utf-8") as f:
                f.write(text)
            return None
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="w+", encoding="utf-8") as f:
            f.write(text)
        return None

    @staticmethod
    def getAria2cPath():
        p = basicFunc.getHerePath() + "/aria2c/aria2c.exe"
        return p

    @staticmethod
    def openFileDialog(caption: str, basedPath: str, filter: str = "全部文件(.*)"):
        filePath, fileType = QFileDialog.getOpenFileName(caption=caption, dir=basedPath, filter=filter)
        return filePath, fileType

    @staticmethod
    def openDirDialog(caption: str, basedPath: str):
        dirPath = QFileDialog.getExistingDirectory(caption=caption, dir=basedPath)
        return dirPath

    @staticmethod
    def getSaveFilePath(caption: str, basedPath: str):
        saveFilePath = QFileDialog.getSaveFileName(caption=caption, dir=basedPath)
        return saveFilePath[0]

    @staticmethod
    def rgb_to_hex(rgb):
        r, g, b = rgb
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        hex_string = '{:02X}{:02X}{:02X}'.format(r, g, b)
        return hex_string



def _iconPath(fileName: str):
    return basicFunc.getHerePath() + f"/data/icon/Icon{fileName}"

def _fontPath(fileName: str):
    return basicFunc.getHerePath() + f"/data/font/{fileName}"


class PIC:
    IconBaiDu = _iconPath("BaiDu.png")
    IconYouDao = _iconPath("YouDao.png")
    IconDownload = _iconPath("Download.png")
    IconHash = _iconPath("Hash.png")
    IconTranslate = _iconPath("Translate.png")

    IconPython = _iconPath("Python.svg")
    IconQt = _iconPath("Qt.png")
    IconQFluentWidgets = _iconPath("QFluentWidgets.png")
    IconGitHub = _iconPath("GitHub.svg")
    IconWriterSide = _iconPath("Writerside.svg")



class fanFont:
    class font:
        def __init__(self, fileName: str, displayName: str, is_file: bool = True):
            self.fileName = fileName
            self.displayName = displayName
            self.is_file = is_file

        @property
        def path(self):
            return _fontPath(self.fileName)

    Hei = font("sans-serif", "默认黑体", is_file = False)
    QingSong = font("清松手写体.ttf", "清松手写体")
    XiangSu = font("中文像素体.ttf", "中文像素体")

