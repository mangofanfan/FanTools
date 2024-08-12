from PySide2 import QtCore
from qfluentwidgets import ComboBoxSettingCard, ColorSettingCard, SettingCardGroup, SwitchSettingCard, ExpandGroupSettingCard, LineEdit, \
    PasswordLineEdit, VBoxLayout, TitleLabel, BodyLabel, SingleDirectionScrollArea, ExpandLayout, qconfig
from qfluentwidgets import Theme, setTheme, ThemeColor, setThemeColor
from qfluentwidgets import FluentIcon as FIC
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QHBoxLayout

import widget.function_setting as funcS


class ConfigPage:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("ConfigPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(200, 200, hData=QSizePolicy.Expanding, vData=QSizePolicy.Expanding)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("ConfigPage")
        self.scrollArea.setWidgetResizable(True)

        self.run()

    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        self.layout.addWidget(label)
        return None

    def run(self):
        self.addTextLine("设置", "Title")
        self.addTextLine("设置项目自动保存在本地，即刻生效，部分设置项目仅对特定功能生效。", "Body")

        # 程序的全局外观设置
        self.CardGroup_Theme = SettingCardGroup("主题设置", self.widget)
        self.Card_ThemeMode = ComboBoxSettingCard(configItem=funcS.cfg.ThemeMode,
                                             icon=FIC.CONSTRACT,
                                             title="主题模式",
                                             content="调整本程序的全局主题模式",
                                             texts=["亮色", "暗色", "跟随系统设置"])
        self.CardGroup_Theme.addSettingCard(self.Card_ThemeMode)
        funcS.cfg.ThemeMode.valueChanged.connect(self.themeChange)
        self.Card_ThemeColor = ColorSettingCard(configItem=funcS.cfg.ThemeColor,
                                                icon=FIC.BACKGROUND_FILL,
                                                title="主题颜色",
                                                content="调整本程序的全局强调色",
                                                enableAlpha=False)
        self.CardGroup_Theme.addSettingCard(self.Card_ThemeColor)
        funcS.cfg.ThemeColor.valueChanged.connect(self.themeColorChange)
        self.layout.addWidget(self.CardGroup_Theme)

        # 程序的全局功能设置
        self.CardGroup_Function = SettingCardGroup("功能", self.widget)
        self.Card_Proxy = SwitchSettingCard(icon=FIC.AIRPLANE,
                                            title="启用代理服务",
                                            content="在通过request调用外部API时添加代理配置。",
                                            configItem=funcS.cfg.ProxyEnable)
        self.CardGroup_Function.addSettingCard(self.Card_Proxy)
        self.ExpandCard_Proxy = ExpandGroupSettingCard(FIC.AIRPLANE,
                                                       "代理服务设置",
                                                       "设置此两项后才能启动代理。",
                                                       self.widget)
        self.CardGroup_Function.addSettingCard(self.ExpandCard_Proxy)
        BodyLabel_ProxyHttp = BodyLabel()
        BodyLabel_ProxyHttp.setText("HTTP代理")
        LineEdit_ProxyHttp = LineEdit()
        LineEdit_ProxyHttp.setFixedWidth(200)
        LineEdit_ProxyHttp.editingFinished.connect(lambda: qconfig.set(funcS.cfg.ProxyHttp, LineEdit_ProxyHttp.text()))
        LineEdit_ProxyHttp.setText(qconfig.get(funcS.cfg.ProxyHttp))
        BodyLabel_ProxyHttps = BodyLabel()
        BodyLabel_ProxyHttps.setText("HTTPS代理")
        LineEdit_ProxyHttps = LineEdit()
        LineEdit_ProxyHttps.setFixedWidth(200)
        LineEdit_ProxyHttps.editingFinished.connect(lambda: qconfig.set(funcS.cfg.ProxyHttps, LineEdit_ProxyHttps.text()))
        LineEdit_ProxyHttps.setText(qconfig.get(funcS.cfg.ProxyHttps))
        self.ExpandCard_Proxy.addGroupWidget(self.expandCardAddWidget(BodyLabel_ProxyHttp, LineEdit_ProxyHttp))
        self.ExpandCard_Proxy.addGroupWidget(self.expandCardAddWidget(BodyLabel_ProxyHttps, LineEdit_ProxyHttps))
        self.layout.addWidget(self.CardGroup_Function)

        # 翻译 API 设置，这些设置需要另外编写保存逻辑。
        self.CardGroup_API = SettingCardGroup("API 设置", self.widget)
        self.layout.addWidget(self.CardGroup_API)

        self.ExpandCard_fanyi_baidu = ExpandGroupSettingCard(icon=FIC.LANGUAGE,
                                            title="百度通用文本翻译API",
                                            content="设置「百度通用文本翻译」的API参数以调用。",
                                            parent=self.widget)
        self.CardGroup_API.addSettingCard(self.ExpandCard_fanyi_baidu)

        BodyLabel_fanyi_baidu_appid = BodyLabel()
        BodyLabel_fanyi_baidu_appid.setText("APP ID")
        BodyLabel_fanyi_baidu_appid.setToolTip("可在百度翻译开放平台获取，需要开通通用文本翻译服务。")
        LineEdit_fanyi_baidu_appid = LineEdit()
        LineEdit_fanyi_baidu_appid.setFixedWidth(200)
        LineEdit_fanyi_baidu_appid.editingFinished.connect(lambda: qconfig.set(funcS.cfg.BaiduAPPID, LineEdit_fanyi_baidu_appid.text()))
        LineEdit_fanyi_baidu_appid.setText(qconfig.get(funcS.cfg.BaiduAPPID))
        self.ExpandCard_fanyi_baidu.addGroupWidget(self.expandCardAddWidget(BodyLabel_fanyi_baidu_appid, LineEdit_fanyi_baidu_appid))

        BodyLabel_fanyi_baidu_key = BodyLabel()
        BodyLabel_fanyi_baidu_key.setText("密钥")
        BodyLabel_fanyi_baidu_key.setToolTip("可在百度翻译开放平台获取，请不要随意向他人展示。<br>翻译工具会将您的密钥保存在本地。")
        LineEdit_fanyi_baidu_key = PasswordLineEdit()
        LineEdit_fanyi_baidu_key.setFixedWidth(200)
        LineEdit_fanyi_baidu_key.editingFinished.connect(lambda: qconfig.set(funcS.cfg.BaiduKey, LineEdit_fanyi_baidu_key.text()))
        LineEdit_fanyi_baidu_key.setText(qconfig.get(funcS.cfg.BaiduKey))
        self.ExpandCard_fanyi_baidu.addGroupWidget(self.expandCardAddWidget(BodyLabel_fanyi_baidu_key, LineEdit_fanyi_baidu_key))

        self.ExpandCard_fanyi_youdao = ExpandGroupSettingCard(icon=FIC.LANGUAGE,
                                                             title="有道文本翻译API",
                                                             content="设置「有道文本翻译」的API参数以调用。",
                                                             parent=self.widget)
        self.CardGroup_API.addSettingCard(self.ExpandCard_fanyi_youdao)

        BodyLabel_fanyi_youdao_appKey = BodyLabel()
        BodyLabel_fanyi_youdao_appKey.setText("APP Key")
        BodyLabel_fanyi_youdao_appKey.setToolTip("可在有道智云AI开放平台获取，需要开通文本翻译服务。")
        LineEdit_fanyi_youdao_appKey = LineEdit()
        LineEdit_fanyi_youdao_appKey.setFixedWidth(200)
        LineEdit_fanyi_youdao_appKey.editingFinished.connect(lambda: qconfig.set(funcS.cfg.YoudaoAPPKey, LineEdit_fanyi_youdao_appKey.text()))
        LineEdit_fanyi_youdao_appKey.setText(qconfig.get(funcS.cfg.YoudaoAPPKey))
        self.ExpandCard_fanyi_youdao.addGroupWidget(self.expandCardAddWidget(BodyLabel_fanyi_youdao_appKey, LineEdit_fanyi_youdao_appKey))

        BodyLabel_fanyi_youdao_key = BodyLabel()
        BodyLabel_fanyi_youdao_key.setText("密钥")
        BodyLabel_fanyi_youdao_key.setToolTip(
            "可在有道智云AI开放平台获取，请不要随意向他人展示。<br>翻译工具会将您的密钥保存在本地。")
        LineEdit_fanyi_youdao_key = PasswordLineEdit()
        LineEdit_fanyi_youdao_key.setFixedWidth(200)
        LineEdit_fanyi_youdao_key.editingFinished.connect(lambda: qconfig.set(funcS.cfg.YoudaoKey, LineEdit_fanyi_youdao_key.text()))
        LineEdit_fanyi_youdao_key.setText(qconfig.get(funcS.cfg.YoudaoKey))
        self.ExpandCard_fanyi_youdao.addGroupWidget(self.expandCardAddWidget(BodyLabel_fanyi_youdao_key, LineEdit_fanyi_youdao_key))

        # 页面底部添加巨大空白
        self.layout.addSpacerItem(self.spacer)

    @staticmethod
    def expandCardAddWidget(label, widget):
        w = QWidget()
        layout = QHBoxLayout(w)
        w.setLayout(layout)
        w.setFixedHeight(50)

        layout.addWidget(label)
        layout.addWidget(widget)
        return w

    @staticmethod
    def themeChange(value: str):
        if value == "light":
            setTheme(Theme.LIGHT)
        elif value == "dark":
            setTheme(Theme.DARK)
        elif value == "auto":
            setTheme(Theme.AUTO)
        else:
            raise
        return None

    @staticmethod
    def themeColorChange(value: str):
        setThemeColor(value)
        return None