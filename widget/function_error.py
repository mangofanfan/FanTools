
class TextIdError(Exception):
    def __init__(self, errorId):
        self.errorId = errorId

    def __str__(self):
        return f"无法翻译指定 ID 的词条：{self.errorId}。"
