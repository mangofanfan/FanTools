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

这是我自己摸索出来的解决方案，目前看来也是我测试的众多猜想中唯一成功的方案。关于滚动页面的技术细节，请参阅 **[滚动页面](Scroll-Page.md)** 。

## 对设计师创建的任意窗口同步程序的全局主题

这是我通过对 qfluentwidgets 的逆向工程（不是）得到的解决方案。

qfluentwidgets 的组件均能适配亮暗主题，我们也可以通过 FluentDesigner 使用 qfluentwidgets 组件可视化地设计窗口，但是如此创建出的窗口是原生 Qt 窗口，本身不能支持亮暗主题切换。当你将程序全局切换成暗色主题时，窗口中的组件都会变色，但窗口本身不会，导致严重的显示问题，完全忍不了呢。

要解决此问题，我们需要修改使用 Designer 生成的窗口代码的方式。我的解决方案是**重写一个窗口类，然后将其作为超类调用。**

<code-block lang="python">
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
</code-block>

导入这两个路径的模块，然后开始重写一个基类，这个类仿照的是我们在前文实现程序窗口框架使用的 FluentWindow，但我们并不需要其导航栏+子页面的功能，以下是最基本、最少的重写：

之所以选择基于qfluentwidgets窗口类重写窗口是因为FluentWindow甚至默认支持Windows 11的云母窗口效果，~~虽然我没找到亚克力窗口效果怎么启用（我感觉不支持，但是qframelesswindow这个库里面是有亚克力效果窗口的，可能还没来得及写吧？）~~ 亚克力效果已经能（部分）实现，请参阅下面的段落。

安装qfluentwidgets会将qframelesswindow作为前置一同安装，这两个库里都有FramelessWindow，小心不要导入错了，否则云母效果会失效并可能出现报错。

<code-block lang="python">
class TranslateWindow(BackgroundAnimationWidget, FramelessWindow):
    def __init__(self, parent=None):
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)
        super().__init__(parent=parent)
    def setMicaEffectEnabled(self, isEnabled: bool):
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return
        self._isMicaEnabled = isEnabled
        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())
        self.setBackgroundColor(self._normalBackgroundColor())
    def isMicaEffectEnabled(self):
        return self._isMicaEnabled
    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
</code-block>

记得`sys`这种模块也要导入才可以，然后把你已经写好的使用由`.ui`文件生成的`.py`文件的代码略作修改，将创建类时使用的超类从`QWidget`更改成我们重写的新类，比如我的是`TranslateWindow`。

<note>我们的类必须要在使用设计师生成的窗口文件之前重写；如果在同一个文件中，则重写的类要放在上面。</note>

此时，窗口的背景颜色已经可以跟随全局主题动态切换，我们的窗口就初具雏形啦！然而仍然有一些问题等待我们处理：

<procedure title="你又发现了如下问题……">
<step>
窗口标题完全消失，窗口右上角的三个功能按钮在深色主题下显示非常奇怪。
</step>
<step>
窗口的大小没有变化，但原本的独立标题栏消失，上面那三个功能按钮可能被设计师里拖拽到程序右上角的组件覆盖遮挡。
</step>
</procedure>

这是因为`FramelessWindow`将窗口原本的标题栏干掉了，然后在窗口内容的顶部部分添加一个透明的标题栏，右边放三个窗口功能按钮。这个重写的标题栏似乎不支持亮暗主题切换，哈！

`FluentWindow`的处理方案是又重写了一个`FluentTitleBar`，非常地合理；既然如此，我们就干脆直接用这个`FluentTitleBar`来节约开发时间……

<code-block lang="python">
self.setTitleBar(FluentTitleBar(self))
</code-block>

`FluentTitleBar`从`qfluentwidgets`直接导入。

至于位置问题，我们可以在Designer中对窗口进行微调，在顶部添加空白空间。

![designer-top-margin](designer-top-margin.png)

42这个数值在我测试是比较OK的，这样我们的多窗口亮暗主题程序就基本成型啦！

![multi-window-light-theme.png](multi-window-light-theme.png)

![multi-window-dark-theme.png](multi-window-dark-theme.png)

然后我们还需要为子窗口添加窗口图标，这时发现图标竟然在窗口标题左边，超出了窗口的边界？解决方案是继承并重写 `FluentTitleBar` 类，为其添加左侧 Margin（没错很像CSS……）

<code-block lang="python">
class FanTitleBar(FluentTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(20, 0, 0, 0)
</code-block>

然后把构造窗口时使用的 `FluentTitleBar` 替换成这个新的 `FanTitleBar` 即可，效果如下。

![translatetoolpage.png](translatetoolpage.png)

等等，这个窗口效果……**亚克力**？

## 为窗口启用亚克力效果

研究了两天qfluentwidgets的窗口之后，我们终于得知了非常惊天的大秘密：qfluentwidgets（不如说是qframelesswindow）是支持云母效果和亚克力效果两种窗口模糊模式的，只是在构建窗口时默认启用的是前者，或者就默认不启用。

qframelesswindow中有一个叫做`AcrylicWindow`的类，可以作为FramelessWindow（是qframelesswindow中的）的替换使用，能够创建无边框、亚克力效果的窗口。qfluentwidgets中的流畅窗口`FluentWindow`经过了几层的继承，最初甚至继承了这个亚克力窗口类，因此理论上是完全可以为窗口启用亚克力效果的。

真正的问题出在`FluentWindow`在继承时只构造了启用云母效果的函数，我们拿代码说话，`FluentWindow`是这样构造的：

<code-block lang="python">
class FluentWindow(FluentWindowBase):
    """ Fluent window """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(FluentTitleBar(self))
        self.navigationInterface = NavigationInterface(self, showReturnButton=True)
        self.widgetLayout = QHBoxLayout()
        # initialize layout
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)
        self.widgetLayout.addWidget(self.stackedWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)
        self.titleBar.raise_()
    def addSubInterface(self, interface: QWidget, icon: Union[FluentIconBase, QIcon, str], text: str,
                        position=NavigationItemPosition.TOP, parent=None, isTransparent=False) -> NavigationTreeWidget:
        ...
    def resizeEvent(self, e):
        ...
</code-block>

我们再返回去看这个`FluentWindowBase`的代码，它是这样构造的：

<code-block lang="python">
class FluentWindowBase(BackgroundAnimationWidget, FramelessWindow):
    """ Fluent window base class """
    def __init__(self, parent=None):
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(240, 244, 249)
        self._darkBackgroundColor = QColor(32, 32, 32)
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.stackedWidget = StackedWidget(self)
        self.navigationInterface = None
        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        FluentStyleSheet.FLUENT_WINDOW.apply(self.stackedWidget)
        # enable mica effect on win11
        self.setMicaEffectEnabled(True)
        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)
    def addSubInterface(self, interface: QWidget, icon: Union[FluentIconBase, QIcon, str], text: str,
                        position=NavigationItemPosition.TOP):
        ...
    def switchTo(self, interface: QWidget):
        ...
    def _onCurrentInterfaceChanged(self, index: int):
        ...
    def _updateStackedBackground(self):
        ...
    def setCustomBackgroundColor(self, light, dark):
        ...
    def _normalBackgroundColor(self):
        ...
    def _onThemeChangedFinished(self):
        ...
    def paintEvent(self, e):
        ...
    def setMicaEffectEnabled(self, isEnabled: bool):
        """ set whether the mica effect is enabled, only available on Win11 """
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return
        self._isMicaEnabled = isEnabled
        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())
        self.setBackgroundColor(self._normalBackgroundColor())
    def isMicaEffectEnabled(self):
        return self._isMicaEnabled
</code-block>

最后两个便是云母效果的启用方法了，我们还能看出云母效果是默认启用的，并且做了系统是否支持的检测（云母效果仅在win11支持）。

然后，这个在qfluentwidgets中定义的`FramelessWindow`是这样构造的：

<code-block lang="python">
if sys.platform != "win32" or sys.getwindowsversion().build < 22000:
    from qframelesswindow import FramelessWindow
else:
    from ctypes.wintypes import MSG
    import win32con
    from PySide2.QtCore import QPoint, QEvent, Qt
    from PySide2.QtGui import QCursor, QMouseEvent
    from PySide2.QtWidgets import QApplication
    from qframelesswindow import AcrylicWindow as Window
    from qframelesswindow.titlebar.title_bar_buttons import TitleBarButtonState
    class FramelessWindow(Window):
        """ Frameless window """
        def __init__(self, parent=None):
            super().__init__(parent)
            self.windowEffect.setMicaEffect(self.winId())
        def nativeEvent(self, eventType, message):
            """ Handle the Windows message """
            msg = MSG.from_address(message.__int__())
            if not msg.hWnd:
                return super().nativeEvent(eventType, message)
            if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
                if self._isHoverMaxBtn():
                    self.titleBar.maxBtn.setState(TitleBarButtonState.HOVER)
                    return True, win32con.HTMAXBUTTON
            elif msg.message in [0x2A2, win32con.WM_MOUSELEAVE]:
                self.titleBar.maxBtn.setState(TitleBarButtonState.NORMAL)
            elif msg.message in [win32con.WM_NCLBUTTONDOWN, win32con.WM_NCLBUTTONDBLCLK] and self._isHoverMaxBtn():
                e = QMouseEvent(QEvent.MouseButtonPress, QPoint(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(self.titleBar.maxBtn, e)
                return True, 0
            elif msg.message in [win32con.WM_NCLBUTTONUP, win32con.WM_NCRBUTTONUP] and self._isHoverMaxBtn():
                e = QMouseEvent(QEvent.MouseButtonRelease, QPoint(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(self.titleBar.maxBtn, e)
            return super().nativeEvent(eventType, message)
        def _isHoverMaxBtn(self):
            pos = QCursor.pos() - self.geometry().topLeft() - self.titleBar.pos()
            return self.titleBar.childAt(pos) is self.titleBar.maxBtn
</code-block>

在不支持的系统上，流畅窗口将不具备云母或亚克力效果，因为其根本的基类是普通的`FramelessWindow`；而在支持的系统上，流畅窗口的基类是`AcrylicWindow`伪装成的`FramelessWindow`，因此可以具备窗口效果。

既然如此，我们只需要也同样继承一个合适的类，然后适当重写启用窗口特效的方法即可实现。遗憾的是，目前尚未能有办法让亚克力窗口完美支持暗色主题，也尚未有办法让流畅窗口这个类真正完美地启用亚克力背景，只能做到让原生Qt窗口（设计师设计出来的窗口）启用亚克力背景。

![AcrylicWindow.png](AcrylicWindow.png)

![AcrylicWindow-2.png](AcrylicWindow-2.png)

