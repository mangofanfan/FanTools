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
    def readFile(file: str):
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="r") as f:
            r = f.read()
        return r

    @staticmethod
    def saveFile(file: str, text: str):
        p = basicFunc.getHerePath() + "/" + file
        with open(file=p, mode="w+") as f:
            f.write(text)
        return None

    @staticmethod
    def getAria2cPath():
        p = basicFunc.getHerePath() + "/aria2c/aria2c.exe"
        return p

    @staticmethod
    def openFileDialog(caption: str, basedPath: str, filter: str):
        filePath, fileType = QFileDialog.getOpenFileName(caption=caption, dir=basedPath, filter=filter)
        return filePath, fileType

    @staticmethod
    def openDirDialog(caption: str, basedPath: str):
        dirPath = QFileDialog.getExistingDirectory(caption=caption, dir=basedPath)
        return dirPath

