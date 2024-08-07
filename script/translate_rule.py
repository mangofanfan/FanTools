# 用户可在此自定义翻译规则，例如保留词条中的固定特定短语不被翻译，但自定义程度有限，复杂的规则仍然需要手工操作完成。
# 程序会将对象 Rule 为每一个提交 API 翻译的词条分别实例化，然后调用其中已经提供的两个函数。
# 不要更改类名 Rule 和已提供的除 __init__() 之外的两个函数名，否则抛出错误可能导致 API 翻译完全失效。
# 程序调用函数 translate_rule() 并提供待翻译的 originalText 作为参数，接收函数的返回值并将其发送给 API 以提交翻译。
# 接收到 API 返回的翻译文本后，再调用函数 reborn_rule() 并提供 targetText 作为参数，接收函数的返回值并将其作为最终文本保留。
# 在这里建立额外的函数甚至类都是可行的，你开心就好~

class Rule:
    def __init__(self):
        self.prefix = ""
        self.prefixes = ["<§bSasha§r> ",
                         "[§eINTERCOM§r] ",
                         "<§bAlan§r> ",
                         "<GDL Scientist> ",
                         "<§cTFA-1541§r> ",
                         "[§6INTERCOM§r] ",
                         "<§dDr. Barney§r> ",
                         "[§6§l!§r] ",
                         "[§6!§r] ",]

    def translate_rule(self, text: str):
        for prefix in self.prefixes:
            if prefix in text:
                text = text.replace(prefix, "")
                self.prefix = prefix
        result = text
        return result

    def reborn_rule(self, text: str):
        result = f"{self.prefix}{text}"
        if "。。。" in result:
            result = result.replace("。。。", "……")
        if "-" in result:
            result = result.replace("-", "——")
        if "TFA——1541" in result:
            result = result.replace("TFA——1541", "TFA-1541")
        if "ON" in result:
            result = result.replace("ON", "启用")
        if "OFF" in result:
            result = result.replace("OFF", "禁用")
        if "冻结隧道" in result:
            result = result.replace("冻结隧道", "冰封隧道")
        if "冰冻隧道" in result:
            result = result.replace("冰冻隧道", "冰封隧道")
        if "氮氧化物" in result:
            result = result.replace("氮氧化物", "Noxesium")
        if "氮钾化物" in result:
            result = result.replace("氮钾化物", "Noxesium")
        if "氮钾" in result:
            result = result.replace("氮钾", "Noxesium")
        if "暗氮" in result:
            result = result.replace("暗氮", "Noxesium")
        if "成绩" in result:
            result = result.replace("成绩", "成就")
        if "成就已锁定" in result:
            result = result.replace("成就已锁定", "成就锁定")
        if "西装" in result:
            result = result.replace("西装", "套装")
        return result


