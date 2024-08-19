from os import getcwd

from PySide2.QtWidgets import QFileDialog


class basicFunc:
    def __init__(self):
        pass

    @staticmethod
    def getHerePath():
        p = getcwd()
        return p

    @staticmethod
    def readFile(file: str, realPath: bool = False):
        if realPath:
            with open(file=file, mode="r") as f:
                r = f.read()
            return r
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="r") as f:
            r = f.read()
        return r

    @staticmethod
    def saveFile(file: str, text: str, realPath: bool = False):
        if realPath:
            with open(file=file, mode="w+") as f:
                f.write(text)
            return None
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="w+") as f:
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
    def rgb_to_hex(rgb):
        r, g, b = rgb
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        hex_string = '{:02X}{:02X}{:02X}'.format(r, g, b)
        return hex_string


class PIC:
    BaiDu = basicFunc.getHerePath() + "/data/baidu.png"
    YouDao = basicFunc.getHerePath() + "/data/youdao.png"

