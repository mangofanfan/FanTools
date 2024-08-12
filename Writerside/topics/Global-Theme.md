# 全局主题 | Global Theme

qfluentwidgets支持程序的全局主题配置。作为高仿winUI的UI库，qfluentwidgets提供的所有新组件都支持全局主题切换。

这个切换包含两个方面，一个是 **「强调色」**（或称为 **「主题色」** ），一个是 **「主题」**。

## 主题 Theme

已知所有由qfluentwidgets提供的组件都是完全支持qfluentwidgets的主题设置的。芒果工具箱的程序主界面是基于FluentWindow构建的，相关代码如下：

<code-block lang="python">
class Main:
    def __init__(self):
        self.mainWindow = FluentWindow()
        self.mainWindow.setMinimumSize(QC.QSize(800, 600))
        self.mainWindow.setWindowTitle("🥭 芒果工具箱 🥭 FanTools  🥭")
        self.mainWindow.setWindowIcon(QIcon(basicFunc.getHerePath() + "\\data\\two_mango_es.png"))
</code-block>

这些代码在Main类中创建了`self.mainwindow`用来充当实例化的`FluentWindow`对象，设置了窗口大小、标题和图标。FluentWindow可以很方便地在左侧边栏添加子页面，并且具有一个全局的「返回」按钮，这些都是封装好的。

虽然如此，FLuentWindow依然只是一个页面框架的封装，里面的每一个子页面都需要我们单独添加，子页面的内容、布局也需要全部自己搞定。

<code-block lang="python">
    def addSubWindow(self):
        self.mainWindow.addSubInterface(interface=window_MainPage.scrollArea,
                                        icon=FIC.HOME,
                                        text="主页")
        self.mainWindow.addSubInterface(interface=window_DownloadPage.scrollArea,
                                        icon=FIC.DOWNLOAD,
                                        text="下载工具")
        self.mainWindow.addSubInterface(interface=window_HashPage.scrollArea,
                                        icon=FIC.ALBUM,
                                        text="哈希值校验工具")
        self.mainWindow.addSubInterface(interface=window_TranslatePage.scrollArea,
                                        icon=FIC.LANGUAGE,
                                        text="翻译工具")
        self.mainWindow.addSubInterface(interface=window_ConfigPage.scrollArea,
                                        icon=FIC.SETTING,
                                        position=NavigationItemPosition.BOTTOM,
                                        text="设置")
    def run(self):
        self.addSubWindow()
        self.mainWindow.show()
</code-block>

如此，我们便成功为FluentWindow实例添加了五个子页面，其中四个在上，一个在下。

将scrollArea作为子页面添加是有考虑的，主要是为实现子页面的滚动。子页面的主体内容依然在一个QWidget内，但这个QWidget被设置在一个scrollArea中，然后再在QWidget内设置一个垂直布局的Layout，再向Layout里面添加组件，从而实现垂直滚动。

这是我自己摸索出来的解决方案，目前看来也是我测试的众多猜想中唯一成功的方案。
