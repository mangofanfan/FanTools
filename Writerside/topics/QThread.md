# 多线程实现 | QThread

## 问题收录与处理方案

<note>
我自己给出的未必都是最佳处理方案，也许只是可行，也许埋了坑，总之先记下来然后放在这里了……
</note>

### 放在 for 循环内的代码只执行了一次

**问题代码**
<code-block lang="python">
class Worker_LoadingStatus(QObject):
    """用来读取词条数据，此时主线程负责更新UI，防止加载过程中UI假死"""
    # TODO：还可以设置加载数量（1-500、501-1000等）来缓解加载耗时
    numberCount = Signal(tuple)
    textList = Signal(list)
    def __init__(self, project: funcT.TranslateProject):
        super().__init__()
        self.cardList = []
        self.project = project
    def run(self):
        n = len(self.project.textList)
        i = 1
        for text in self.project.textList:
            text: funcT.TranslateText
            print(i, text)
            card = TranslateTextCard(titleLabel=str(text.id))
            self.cardList.append(card)
            self.numberCount.emit(i, n)
            i += 1
        self.textList.emit(self.cardList)
        return None
</code-block>

这是通过QThread实现的子线程将要执行的代码，用于读取翻译工具保存的工程文件，用于在列表词条翻译器中以列表形式显示。

在编写调试的过程中意外发现，这里的代码运行有问题，子线程成功跑起了`run()`方法，但是for循环内的代码只执行了一次。

因为控制台只输出了一次：

    1 <widget.function_translate.TranslateText object at 0x000001EC322E0430>

逻辑上，每读取一个词条，线程都会发送一个`numberCount`信号返回给主线程，主线程据此更新进度条，并在接收到最后的`textList`信号后将处理好的列表用于列表翻译器的页面显示。

那么这个链条是哪里出了问题呢？

请注意，由于`numberCount`信号发送的数据类型是tuple，一个tuple应该单独用小括号包起来，而我在发送信号时简单地写成了：

<code-block lang="python">self.numberCount.emit(i, n)</code-block>

于是由于类型错误，这里的代码在运行第一个循环的过程中就已经报错，子线程实际上已经挂掉了，但我们并不知道。

将代码作如下修改后，问题解决：

<code-block lang="python">self.numberCount.emit((i, n))</code-block>

此时控制台会不断打印每一个词条的读取信息直到全部完成，并且窗口UI没有假死，说明我们的计划成功啦！

**这给我们的思考是，若QThread子线程中的循环没有按照我们的预期进行，例如只执行了一次就无了，有可能是循环体中存在代码错误，导致抛出异常而结束。**

### 跨线程的UI组件

然后在继续处理上面的案例时遇到了下列异常情况：

![error-window](error-window.png)

<procedure title="问题复现">
<step>
子线程已经处理完毕所有翻译词条，并且为每个词条生成了一个卡片组件。
</step>
<step>
所有的卡片组件已经被放入一个列表中，并且列表已经被通过信号传递给主线程。
</step>
<step>
主线程从列表中提取卡片组件，并将其父对象重设为窗口中的对应元素，添加layout。
</step>
<step>
异常情况如图所示。
</step>
</procedure>

可以看出，我们期待的这一千多张卡片并没有在窗口的对应位置排列开来，而是个个都成为了独立窗口，直接把我的任务栏给干愣住了。

事有蹊跷，返工排查，我发现若是在主线程中直接创建卡片，完全没有问题；但在子线程中创建的卡片，发送到主线程后便必然出现此问题。

注意，此时Pycharm中的Python控制台没有任何报错信息。根据以往遇到无报错信息问题的惯例，我们知道将控制台模式设置为「模拟终端」可能会让报错信息显示出来。

再次运行出错的步骤，我们得到如下输出：

<code-block>
QObject::setParent: Cannot set parent, new parent is in a different thread
</code-block>

**也就是说，在一个线程中的一个UI组件一经创建，其父对象便无法更改至其他的线程。**

**进一步测试后我们得知，在一个线程中创建UI组件时，不可以将该组件的父对象手动设置成其他线程中的对象。**

这样一来我的整个多线程防假死的逻辑就完全不可行了，返工重写喽~