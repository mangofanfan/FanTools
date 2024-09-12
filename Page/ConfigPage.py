import logging
from functools import partial

from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout, QBoxLayout
from qfluentwidgets import ComboBoxSettingCard, ColorSettingCard, SettingCardGroup, SwitchSettingCard, \
    ExpandGroupSettingCard, LineEdit, \
    PasswordLineEdit, VBoxLayout, TitleLabel, BodyLabel, SingleDirectionScrollArea, qconfig, ToolTipFilter, \
    OptionsSettingCard, RangeSettingCard, CheckBox
from qfluentwidgets import FluentIcon as FIC
from qfluentwidgets import Theme, setTheme, setThemeColor

from widget.function_setting import cfg, ProxySettingCard, BaiDuAPISettingCard, YouDaoAPISettingCard
from widget.function import PIC

logger = logging.getLogger("FanTools.ConfigPage")


class ConfigPage:
    def __init__(self):
        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName("ConfigPage")
        self._layout = QVBoxLayout()
        self.bodyWidget.setLayout(self._layout)
        self._layout.setContentsMargins(0, 5, 0, 0)

        self.widget = QFrame()
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setWidgetResizable(True)

        self.addTextLine("设置", "Title", self._layout)
        self.addTextLine("设置项目自动保存在本地，未标注的项目都将即刻生效。", "Body")
        self._layout.addWidget(self.scrollArea)

        self.run()
        logger.debug("页面初始化完毕。")

    def addTextLine(self, text: str, labelType: str = "Body", layout: QBoxLayout = None):
        if labelType == "Title":
            label = TitleLabel()
            label.setAlignment(Qt.AlignCenter)
        else:
            label = BodyLabel()
        label.setText(text)
        if layout:
            layout.addWidget(label)
        else:
            self.layout.addWidget(label)
        return None

    def run(self):
        # 程序的全局外观设置
        self.CardGroup_Theme = SettingCardGroup("主题设置", self.widget)
        self.Card_ThemeMode = ComboBoxSettingCard(configItem=cfg.ThemeMode,
                                                  icon=FIC.CONSTRACT,
                                                  title="主题模式",
                                                  content="调整本程序的全局主题模式",
                                                  texts=["亮色", "暗色", "跟随系统设置"])
        self.CardGroup_Theme.addSettingCard(self.Card_ThemeMode)
        cfg.ThemeMode.valueChanged.connect(self.themeChange)
        self.Card_ThemeColor = ColorSettingCard(configItem=cfg.ThemeColor,
                                                icon=FIC.BACKGROUND_FILL,
                                                title="主题颜色",
                                                content="调整本程序的全局强调色",
                                                enableAlpha=False)
        self.CardGroup_Theme.addSettingCard(self.Card_ThemeColor)
        cfg.ThemeColor.valueChanged.connect(self.themeColorChange)
        self.Card_WindowAcrylicEnable = SwitchSettingCard(title="启用亚克力效果（重启后生效，不稳定）",
                                                          content="为工具箱的所有窗口启用亚克力效果（实时计算的半透明虚化窗口背景，深色模式显示可能存在异常）",
                                                          configItem=cfg.WindowAcrylicEnable,
                                                          icon=FIC.FIT_PAGE)
        self.CardGroup_Theme.addSettingCard(self.Card_WindowAcrylicEnable)
        self.Card_FontFamily = ComboBoxSettingCard(configItem=cfg.FontFamily,
                                                   title="应用程序字体（重启后生效）",
                                                   content="除设置卡片与弹出窗口外，字体在程序内全局生效",
                                                   icon=FIC.FONT,
                                                   texts=["默认黑体", "中文像素体", "清松手写体"])
        self.CardGroup_Theme.addSettingCard(self.Card_FontFamily)
        self.layout.addWidget(self.CardGroup_Theme)

        # 程序的全局功能设置
        self.CardGroup_Function = SettingCardGroup("功能", self.widget)
        self.Card_EditConfirm = SwitchSettingCard(icon=FIC.QUESTION,
                                                  title="退出程序时确认",
                                                  content="在用户退出程序时弹出窗口确认，提供取消的机会。",
                                                  configItem=cfg.ExitConfirm)
        self.CardGroup_Function.addSettingCard(self.Card_EditConfirm)
        # 代理开关
        self.Card_Proxy = SwitchSettingCard(icon=FIC.AIRPLANE,
                                            title="启用代理服务",
                                            content="在通过request调用外部API时添加代理配置。",
                                            configItem=cfg.ProxyEnable)
        self.Card_Proxy.setToolTip("如果明明已经联网，程序在调用 Web API 时却屡屡无法成功，您可能需要开启此项。\n"
                                   "若为本机代理，只需要修改冒号后的端口号即可。")
        self.Card_Proxy.installEventFilter(ToolTipFilter(self.Card_Proxy))
        self.CardGroup_Function.addSettingCard(self.Card_Proxy)
        # 代理服务设置
        self.Card_ProxySetting = ProxySettingCard()
        self.CardGroup_Function.addSettingCard(self.Card_ProxySetting)

        self.Card_YiYanEnable = SwitchSettingCard(configItem=cfg.YiYanEnable,
                                                  icon=FIC.PASTE,
                                                  title="启用一言功能",
                                                  content="如果关闭此项，所有一言卡片都将显示默认文本。")
        self.CardGroup_Function.addSettingCard(self.Card_YiYanEnable)
        self.Card_YiYanAPI = OptionsSettingCard(configItem=cfg.YiYanAPI,
                                                icon=FIC.APPLICATION,
                                                title="一言API接口",
                                                content="选择「一言」功能的调用接口，芒果自建了一个镜像接口以便在官方接口失效时使用",
                                                texts=["官方接口 - hitokoto.cn", "帆域接口 - mangofanfan.cn"])
        self.CardGroup_Function.addSettingCard(self.Card_YiYanAPI)
        self.ExpandCard_YiYanType = ExpandGroupSettingCard(icon=FIC.TAG,
                                                           title="一言类型",
                                                           content="调用一言时可以指定调用所得句子的分类，可以多选，完全不选等于全选。",
                                                           parent=self.widget)
        self.CardGroup_Function.addSettingCard(self.ExpandCard_YiYanType)
        self.Card_TimeSleep = RangeSettingCard(configItem=cfg.TimeSleep,
                                               title="在线资源刷新间隔（数值单位1s）",
                                               content="控制「一言」等模块的刷新间隔",
                                               icon=FIC.SEND)
        self.CardGroup_Function.addSettingCard(self.Card_TimeSleep)
        self.layout.addWidget(self.CardGroup_Function)

        BodyLabel_YiYanTypeA = BodyLabel()
        BodyLabel_YiYanTypeA.setText("我们一直在一起，所以最后也想在你身旁。——火影忍者")
        CheckBox_YiYanTypeA = CheckBox()
        CheckBox_YiYanTypeA.setText("动画（a）")
        CheckBox_YiYanTypeA.setChecked(cfg.get(cfg.YiYanTypeA))
        CheckBox_YiYanTypeA.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeA, CheckBox_YiYanTypeA.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeA, CheckBox_YiYanTypeA))

        BodyLabel_YiYanTypeB = BodyLabel()
        BodyLabel_YiYanTypeB.setText("不管你说再多的慌，只有自己的内心，是无法欺骗的啊。——七大罪")
        CheckBox_YiYanTypeB = CheckBox()
        CheckBox_YiYanTypeB.setText("漫画（b）")
        CheckBox_YiYanTypeB.setChecked(cfg.get(cfg.YiYanTypeB))
        CheckBox_YiYanTypeB.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeB, CheckBox_YiYanTypeB.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeB, CheckBox_YiYanTypeB))

        BodyLabel_YiYanTypeC = BodyLabel()
        BodyLabel_YiYanTypeC.setText("断剑重铸之日，骑士归来之时。——锐雯 - 英雄联盟")
        CheckBox_YiYanTypeC = CheckBox()
        CheckBox_YiYanTypeC.setText("游戏（c）")
        CheckBox_YiYanTypeC.setChecked(cfg.get(cfg.YiYanTypeC))
        CheckBox_YiYanTypeC.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeC, CheckBox_YiYanTypeC.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeC, CheckBox_YiYanTypeC))

        BodyLabel_YiYanTypeD = BodyLabel()
        BodyLabel_YiYanTypeD.setText("所谓家嘛，就是一个能让你懒惰、晕眩、疯狂放松的地方。——龙应台 - 亲爱的安德烈")
        CheckBox_YiYanTypeD = CheckBox()
        CheckBox_YiYanTypeD.setText("文学（d）")
        CheckBox_YiYanTypeD.setChecked(cfg.get(cfg.YiYanTypeD))
        CheckBox_YiYanTypeD.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeD, CheckBox_YiYanTypeD.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeD, CheckBox_YiYanTypeD))

        BodyLabel_YiYanTypeE = BodyLabel()
        BodyLabel_YiYanTypeE.setText("不要太在意，太在意会开始害怕失去。——Cherri")
        CheckBox_YiYanTypeE = CheckBox()
        CheckBox_YiYanTypeE.setText("原创（e）")
        CheckBox_YiYanTypeE.setChecked(cfg.get(cfg.YiYanTypeE))
        CheckBox_YiYanTypeE.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeE, CheckBox_YiYanTypeE.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeE, CheckBox_YiYanTypeE))

        BodyLabel_YiYanTypeF = BodyLabel()
        BodyLabel_YiYanTypeF.setText("和谐的生活离不开摸头和被摸头。——豆瓣网友")
        CheckBox_YiYanTypeF = CheckBox()
        CheckBox_YiYanTypeF.setText("来自网络（f）")
        CheckBox_YiYanTypeF.setChecked(cfg.get(cfg.YiYanTypeF))
        CheckBox_YiYanTypeF.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeF, CheckBox_YiYanTypeF.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeF, CheckBox_YiYanTypeF))

        BodyLabel_YiYanTypeG = BodyLabel()
        BodyLabel_YiYanTypeG.setText("日出而作，日入而息。——击壤歌")
        CheckBox_YiYanTypeG = CheckBox()
        CheckBox_YiYanTypeG.setText("其他（g）")
        CheckBox_YiYanTypeG.setChecked(cfg.get(cfg.YiYanTypeG))
        CheckBox_YiYanTypeG.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeG, CheckBox_YiYanTypeG.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeG, CheckBox_YiYanTypeG))

        BodyLabel_YiYanTypeH = BodyLabel()
        BodyLabel_YiYanTypeH.setText("看看人间的苦难，听听人民的呐喊！——《悲惨世界》")
        CheckBox_YiYanTypeH = CheckBox()
        CheckBox_YiYanTypeH.setText("影视（h）")
        CheckBox_YiYanTypeH.setChecked(cfg.get(cfg.YiYanTypeH))
        CheckBox_YiYanTypeH.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeH, CheckBox_YiYanTypeH.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeH, CheckBox_YiYanTypeH))

        BodyLabel_YiYanTypeI = BodyLabel()
        BodyLabel_YiYanTypeI.setText("晚日寒鸦一片愁。柳塘新绿却温柔。——辛弃疾 - 鹧鸪天·晚日寒鸦一片愁")
        CheckBox_YiYanTypeI = CheckBox()
        CheckBox_YiYanTypeI.setText("诗词（i）")
        CheckBox_YiYanTypeI.setChecked(cfg.get(cfg.YiYanTypeI))
        CheckBox_YiYanTypeI.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeI, CheckBox_YiYanTypeI.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeI, CheckBox_YiYanTypeI))

        BodyLabel_YiYanTypeJ = BodyLabel()
        BodyLabel_YiYanTypeJ.setText("飒爽英姿闯江湖，诗酒茶话莫孤独。——岚")
        CheckBox_YiYanTypeJ = CheckBox()
        CheckBox_YiYanTypeJ.setText("网易云（j）")
        CheckBox_YiYanTypeJ.setChecked(cfg.get(cfg.YiYanTypeJ))
        CheckBox_YiYanTypeJ.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeJ, CheckBox_YiYanTypeJ.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeJ, CheckBox_YiYanTypeJ))

        BodyLabel_YiYanTypeK = BodyLabel()
        BodyLabel_YiYanTypeK.setText("眼睛是心灵的窗户。——达芬奇")
        CheckBox_YiYanTypeK = CheckBox()
        CheckBox_YiYanTypeK.setText("哲学（k）")
        CheckBox_YiYanTypeK.setChecked(cfg.get(cfg.YiYanTypeK))
        CheckBox_YiYanTypeK.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeK, CheckBox_YiYanTypeK.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeK, CheckBox_YiYanTypeK))

        BodyLabel_YiYanTypeL = BodyLabel()
        BodyLabel_YiYanTypeL.setText("大本钟下送快递——上面摆，下面寄。——饭堂周末夜")
        CheckBox_YiYanTypeL = CheckBox()
        CheckBox_YiYanTypeL.setText("抖机灵（l）")
        CheckBox_YiYanTypeL.setChecked(cfg.get(cfg.YiYanTypeL))
        CheckBox_YiYanTypeL.stateChanged.connect(lambda: cfg.set(cfg.YiYanTypeL, CheckBox_YiYanTypeL.isChecked()))
        self.ExpandCard_YiYanType.addGroupWidget(self.expandCardAddWidget(BodyLabel_YiYanTypeL, CheckBox_YiYanTypeL))

        # 翻译设置
        self.CardGroup_API = SettingCardGroup("翻译工具", self.widget)
        self.layout.addWidget(self.CardGroup_API)

        self.GlobalEnableGlossary = SwitchSettingCard(configItem=cfg.GlossaryEnable,
                                                      title="启用术语表",
                                                      content="翻译工具全局启用术语表，术语表的详细设置需要在术语表窗口中设置。",
                                                      icon=FIC.ERASE_TOOL)
        self.CardGroup_API.addSettingCard(self.GlobalEnableGlossary)

        self.Card_BaiDuAPI = BaiDuAPISettingCard(self.widget)
        self.CardGroup_API.addSettingCard(self.Card_BaiDuAPI)
        self.Card_YouDaoAPI = YouDaoAPISettingCard(self.widget)
        self.CardGroup_API.addSettingCard(self.Card_YouDaoAPI)

        self.layout.addStretch()

    @staticmethod
    def expandCardAddWidget(label, widget):
        w = QWidget()
        layout = QHBoxLayout(w)
        w.setLayout(layout)
        w.setFixedHeight(50)

        widget.setMaximumWidth(200)
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
        logger.info(f"由于设置变动，程序主题已更改为 {value}")
        return None

    @staticmethod
    def themeColorChange(value: str):
        setThemeColor(value)
        logger.info(f"由于设置变动，程序主题色已更改为 {value}")
        return None