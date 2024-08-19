# 其他错误修复 | Other-Bugfixing

## 进程已结束，退出代码为 -1073740940 (0xC0000374) | Process finished with exit code -1073740940 (0xC0000374)

出现此错误的具体原因无法明了。我的报错位置在程序结束时，调试得知是「**正好在程序结束时**」，也就是调用`sys.exit()`时（我已经将`app.exec_()`独立成行，可以排除是Qt事件循环中出现问题）。将`sys.exit()`换成`exit()`、`quit()`、`QApplication.quit()`或直接引发异常`SystemExit`**均不能阻止问题出现**。

通过搜索引擎，我们得知此错误是 Windows 内存堆损坏，别问我这是什么意思因为我也不知道。通过简单的排查，确定**问题不是PySide2或qfluentwidgets本身导致**，那么问题就出在我们自己编写的代码中。

<note>已经尝试在Windows时区设置中启用「为全球语言提供Unicode8支持」，无效（我这个设置本来就是启用的）。</note>

接下来就是排除法，我们在程序入口`main.py`中逐步减少加载的代码量，在确保程序成功运行不会报错的前提下依次将代码行注释掉，如此直到不再报错，便可以推断出是哪一行代码导致的问题。

排查的过程就免了，结果是，来自`MainPage.py`的类`MainPage`实例化，会导致程序结束时产生此报错。

接下来战略转进到这个代码段，继续重复排除过程，发现真正的问题在于在页面上添加了两个`spacer`，删除一个之后问题解决。

好奇怪，不知道为什么，决定用脑子来想。

## TableWidget组件，枚举删除行、列时出错 NoneType

这个是逻辑上的问题，假如我们拥有一个表格，并需要提供一种方法，能够遍历表格中所有的行，如果这个行是空行就把它删掉。

![translate-tablewidget.png](translate-tablewidget.png)

我把功能写在右键菜单里了，这个的相关信息在[右键菜单](Right-Click-Menu.md)页面。在实现上，我们继承了 `TableWidget` 类，直接在其 `__init__()` 中实现表格的构建。

为下方的删除空行按钮绑定函数的构造如下：

<code-block lang="python">
    def deleteBlank(self):
        for i in range(self.rowCount():
            if not self.item(i, 0).text() and not self.item(i, 1).text():
                self.removeRow(i)
                continue
        return None
</code-block>

逻辑上是遍历每一行，只要这一行没有内容就删，想法非常好，但是运行起来则会报错。问题出在以下两个方面：
* 在表格中的某一格x，y内没有任何内容时，方法 `self.item(x, y)` 会得到 `None`，于是我们得到了类型错误；
* 实际上在行数大于1的时候，我们无法遍历所有行：两行则剩下一行，五行则剩下两行……

第一点好办，只要将 `.text()` 去掉就可以了，第二点问题呢我先把修复过的代码放下来，大家一眼就能看出问题所在：

<code-block lang="python">
    def deleteBlank(self):
        l = list(range(self.rowCount()))
        l.reverse()
        for i in l:
            if not self.item(i, 0) and not self.item(i, 1):
                self.removeRow(i)
                continue
        return None
</code-block>

**没错！我们需要把`range`得到的列表倒序翻转一下，相当于从最后一行向前枚举！** 这是由于如果从前往后枚举，比如我们删除了空的第一行，那么下一步我们枚举得到的第二行则是原表格的第三行，原表格的第二行现在成为了第一行，我们就把这一行跳过了。

嗯，就酱。
