from PySide2.QtGui import QFontDatabase

from widget.function import fanFont
from widget.function_setting import cfg


def getFontStyleSheet(font: fanFont.font = None):
    if not font:
        ff = cfg.get(cfg.FontFamily)
        if ff == "Hei":
            font = fanFont.Hei
        elif ff == "XiangSu":
            font = fanFont.XiangSu
        elif ff == "QingSong":
            font = fanFont.QingSong
        else:
            raise
    if font.is_file is True:
        fontDb = QFontDatabase()
        fontId = fontDb.addApplicationFont(font.path)
        fontFamilies = fontDb.applicationFontFamilies(fontId)[0]
    else:
        fontFamilies = font.fileName
    fontStyleSheet = "* { font-family: '{font}'; }".replace("{font}", fontFamilies)
    return fontStyleSheet