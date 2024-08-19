# 其他错误修复 | Other-Bugfixing

## 进程已结束，退出代码为 -1073740940 (0xC0000374) | Process finished with exit code -1073740940 (0xC0000374)

出现此错误的具体原因无法明了。我的报错位置在程序结束时，调试得知是「**正好在程序结束时**」，也就是调用`sys.exit()`时（我已经将`app.exec_()`独立成行，可以排除是Qt事件循环中出现问题）。将`sys.exit()`换成`exit()`、`quit()`、`QApplication.quit()`或直接引发异常`SystemExit`**均不能阻止问题出现**。

通过搜索引擎，我们得知此错误是 Windows 内存堆损坏，别问我这是什么意思因为我也不知道。通过简单的排查，确定**问题不是PySide2或qfluentwidgets本身导致**，那么问题就出在我们自己编写的代码中。

<note>已经尝试在Windows时区设置中启用「为全球语言提供Unicode8支持」，无效（我这个设置本来就是启用的）。</note>

接下来就是排除法，我们在程序入口`main.py`中逐步减少加载的代码量，在确保程序成功运行不会报错的前提下依次将代码行注释掉，如此直到不再报错，便可以推断出是哪一行代码导致的问题。

排查的过程就免了，结果是，来自`MainPage.py`的类`MainPage`实例化，会导致程序结束时产生此报错。

接下来战略转进到这个代码段，继续重复排除过程，发现真正的问题在于在页面上添加了两个`spacer`，删除一个之后问题解决。

好奇怪，不知道为什么，决定用脑子来想。