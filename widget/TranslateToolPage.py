# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TranslateToolPage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from qfluentwidgets import ComboBox
from qfluentwidgets import PushButton
from qfluentwidgets import PrimaryPushButton
from qfluentwidgets import SplitPushButton
from qfluentwidgets import ToolButton
from qfluentwidgets import ToggleButton
from qfluentwidgets import CaptionLabel
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import TextEdit
from qfluentwidgets import TableWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.NonModal)
        Form.resize(1003, 477)
        Form.setAutoFillBackground(False)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 42, -1, -1)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.SubtitleLabel = SubtitleLabel(Form)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")

        self.horizontalLayout_7.addWidget(self.SubtitleLabel)

        self.SplitPushButton = SplitPushButton(Form)
        self.SplitPushButton.setObjectName(u"SplitPushButton")

        self.horizontalLayout_7.addWidget(self.SplitPushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.TextEdit_OriginalText = TextEdit(Form)
        self.TextEdit_OriginalText.setObjectName(u"TextEdit_OriginalText")
        self.TextEdit_OriginalText.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.TextEdit_OriginalText)

        self.TextEdit_TranslatedText = TextEdit(Form)
        self.TextEdit_TranslatedText.setObjectName(u"TextEdit_TranslatedText")

        self.horizontalLayout_2.addWidget(self.TextEdit_TranslatedText)

        self.TableWidget = TableWidget(Form)
        self.TableWidget.setObjectName(u"TableWidget")
        self.TableWidget.setShowGrid(False)

        self.horizontalLayout_2.addWidget(self.TableWidget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.PushButton_OneBefore = PushButton(Form)
        self.PushButton_OneBefore.setObjectName(u"PushButton_OneBefore")

        self.horizontalLayout.addWidget(self.PushButton_OneBefore)

        self.PushButton_OneNext = PushButton(Form)
        self.PushButton_OneNext.setObjectName(u"PushButton_OneNext")

        self.horizontalLayout.addWidget(self.PushButton_OneNext)

        self.PrimaryPushButton_SaveAndContinue = PrimaryPushButton(Form)
        self.PrimaryPushButton_SaveAndContinue.setObjectName(u"PrimaryPushButton_SaveAndContinue")

        self.horizontalLayout.addWidget(self.PrimaryPushButton_SaveAndContinue)

        self.PrimaryPushButton_MarkAndContinue = PrimaryPushButton(Form)
        self.PrimaryPushButton_MarkAndContinue.setObjectName(u"PrimaryPushButton_MarkAndContinue")

        self.horizontalLayout.addWidget(self.PrimaryPushButton_MarkAndContinue)

        self.ToolButton_CopyOriginalText = ToolButton(Form)
        self.ToolButton_CopyOriginalText.setObjectName(u"ToolButton_CopyOriginalText")

        self.horizontalLayout.addWidget(self.ToolButton_CopyOriginalText)

        self.ToolButton_SearchInWeb = ToolButton(Form)
        self.ToolButton_SearchInWeb.setObjectName(u"ToolButton_SearchInWeb")

        self.horizontalLayout.addWidget(self.ToolButton_SearchInWeb)

        self.ToolButton_ClearTranslatedText = ToolButton(Form)
        self.ToolButton_ClearTranslatedText.setObjectName(u"ToolButton_ClearTranslatedText")

        self.horizontalLayout.addWidget(self.ToolButton_ClearTranslatedText)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PrimaryPushButton_UseAPIText = PrimaryPushButton(Form)
        self.PrimaryPushButton_UseAPIText.setObjectName(u"PrimaryPushButton_UseAPIText")

        self.verticalLayout.addWidget(self.PrimaryPushButton_UseAPIText)

        self.PushButton_EditPrompt = PushButton(Form)
        self.PushButton_EditPrompt.setObjectName(u"PushButton_EditPrompt")
        self.PushButton_EditPrompt.setMinimumSize(QSize(180, 0))

        self.verticalLayout.addWidget(self.PushButton_EditPrompt)

        self.PushButton_Glossary = PushButton(Form)
        self.PushButton_Glossary.setObjectName(u"PushButton_Glossary")

        self.verticalLayout.addWidget(self.PushButton_Glossary)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.TextEdit_API = TextEdit(Form)
        self.TextEdit_API.setObjectName(u"TextEdit_API")
        self.TextEdit_API.setMinimumSize(QSize(0, 130))
        self.TextEdit_API.setMaximumSize(QSize(16777215, 130))

        self.horizontalLayout_3.addWidget(self.TextEdit_API)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetMaximumSize)
        self.PrimaryPushButton_TranslateWithAPI = PrimaryPushButton(Form)
        self.PrimaryPushButton_TranslateWithAPI.setObjectName(u"PrimaryPushButton_TranslateWithAPI")

        self.verticalLayout_4.addWidget(self.PrimaryPushButton_TranslateWithAPI)

        self.ComboBox_API = ComboBox(Form)
        self.ComboBox_API.setObjectName(u"ComboBox_API")

        self.verticalLayout_4.addWidget(self.ComboBox_API)

        self.ToggleButton_AutoTranslateWithAPI = ToggleButton(Form)
        self.ToggleButton_AutoTranslateWithAPI.setObjectName(u"ToggleButton_AutoTranslateWithAPI")
        self.ToggleButton_AutoTranslateWithAPI.setMinimumSize(QSize(180, 0))

        self.verticalLayout_4.addWidget(self.ToggleButton_AutoTranslateWithAPI)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.PushButton_SaveProject = PushButton(Form)
        self.PushButton_SaveProject.setObjectName(u"PushButton_SaveProject")

        self.horizontalLayout_4.addWidget(self.PushButton_SaveProject)

        self.PushButton_ViewProject = PushButton(Form)
        self.PushButton_ViewProject.setObjectName(u"PushButton_ViewProject")

        self.horizontalLayout_4.addWidget(self.PushButton_ViewProject)

        self.CaptionLabel = CaptionLabel(Form)
        self.CaptionLabel.setObjectName(u"CaptionLabel")

        self.horizontalLayout_4.addWidget(self.CaptionLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        Form.setProperty("lightCustomQss", "")
        Form.setProperty("darkCustomQss", "")
        self.SubtitleLabel.setText(QCoreApplication.translate("Form", u"Subtitle label", None))
#if QT_CONFIG(tooltip)
        self.SplitPushButton.setToolTip(QCoreApplication.translate("Form", u"\u4e0b\u62c9\u9009\u62e9\u5feb\u901f\u64cd\u4f5c\u7c7b\u578b", None))
#endif // QT_CONFIG(tooltip)
        self.SplitPushButton.setProperty("text_", QCoreApplication.translate("Form", u"\u4e0b\u62c9\u9009\u62e9\u5feb\u901f\u64cd\u4f5c\u7c7b\u578b", None))
        self.TextEdit_TranslatedText.setPlaceholderText(QCoreApplication.translate("Form", u"\u5728\u6b64\u5904\u8f93\u5165\u5de6\u8fb9\u8bcd\u6761\u7684\u7ffb\u8bd1\u6587\u672c\u2026\u2026", None))
        self.PushButton_OneBefore.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u6761", None))
        self.PushButton_OneNext.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u6761", None))
#if QT_CONFIG(tooltip)
        self.PrimaryPushButton_SaveAndContinue.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u4f7f\u7528\u4e0a\u65b9\u7684\u4eba\u5de5\u7ffb\u8bd1\u6587\u672c\u4f5c\u4e3a\u8bd1\u6587\u4fdd\u5b58\u3002</p><p>\u540c\u65f6\u6dfb\u52a0\u6807\u7b7e\u300c\u4eba\u5de5\u7ffb\u8bd1\u300d\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PrimaryPushButton_SaveAndContinue.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.PrimaryPushButton_MarkAndContinue.setText(QCoreApplication.translate("Form", u"\u6807\u8bb0", None))
#if QT_CONFIG(tooltip)
        self.ToolButton_CopyOriginalText.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5c06\u5de6\u4fa7\u7684\u539f\u6587\u590d\u5236\u4e3a\u53f3\u4fa7\u7684\u8bd1\u6587\uff0c\u9002\u7528\u4e8e\u683c\u5f0f\u4ee3\u7801\u590d\u6742\u7684\u6587\u672c\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_SearchInWeb.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5728\u7cfb\u7edf\u9ed8\u8ba4\u6d4f\u89c8\u5668\u4e2d\u6253\u5f00\u5e76\u641c\u7d22\u5f85\u7ffb\u8bd1\u6587\u672c\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_ClearTranslatedText.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u6e05\u7a7a\u53f3\u4fa7\u7684\u5f85\u7ffb\u8bd1\u6587\u672c\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.PrimaryPushButton_UseAPIText.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5c06\u901a\u8fc7 API \u83b7\u53d6\u7684\u7ffb\u8bd1\u5e94\u7528\u5230\u8be5\u8bcd\u6761\uff0c\u8fd9\u5c06\u81ea\u52a8\u4fdd\u5b58\u8bcd\u6761\u5e76\u6dfb\u52a0\u6807\u7b7e\u3002</p><p>\u5728\u5e94\u7528\u4e4b\u524d\uff0c\u60a8\u4ecd\u7136\u53ef\u4ee5\u5728\u53f3\u4fa7\u6587\u672c\u6846\u4e2d\u7f16\u8f91 API \u83b7\u53d6\u7684\u7ffb\u8bd1\u5b57\u6bb5\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PrimaryPushButton_UseAPIText.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528\u8fd9\u4e2a\u7ffb\u8bd1", None))
#if QT_CONFIG(tooltip)
        self.PushButton_EditPrompt.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>prompt \u7528\u4e8e\u5411 AI \u9610\u8ff0\u5b83\u7684\u8eab\u4efd\u3001\u4efb\u52a1\u4e0e\u6ce8\u610f\u4e8b\u9879\u3002</p><p>\u5982\u6309\u9ed8\u8ba4\u8bbe\u7f6e\u8c03\u7528 AI \u7ffb\u8bd1\u6ca1\u6709\u663e\u8457\u7684\u95ee\u9898\uff0c\u4fdd\u6301\u9ed8\u8ba4\u5373\u53ef\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PushButton_EditPrompt.setText(QCoreApplication.translate("Form", u"[AI\u4e13\u7528] \u7f16\u8f91 prompt", None))
#if QT_CONFIG(tooltip)
        self.PushButton_Glossary.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u914d\u7f6e API \u4e4b\u540e\u624d\u80fd\u8c03\u7528 API \u5e76\u7ffb\u8bd1\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PushButton_Glossary.setText(QCoreApplication.translate("Form", u"\u672f\u8bed\u8868", None))
        self.TextEdit_API.setPlaceholderText(QCoreApplication.translate("Form", u"API\u5f97\u5230\u7684\u7ffb\u8bd1\u7ed3\u679c\u5c06\u5728\u6b64\u5904\u663e\u793a\uff0c\u5e76\u81ea\u52a8\u5e94\u7528\u672f\u8bed\u8868\u7ed3\u679c\u3002", None))
        self.PrimaryPushButton_TranslateWithAPI.setText(QCoreApplication.translate("Form", u"\u8c03\u7528API\u6267\u884c\u7ffb\u8bd1", None))
#if QT_CONFIG(tooltip)
        self.ToggleButton_AutoTranslateWithAPI.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u6fc0\u6d3b\u81ea\u52a8\u7ffb\u8bd1\u671f\u95f4\uff0c\u60a8\u5c06\u65e0\u6cd5\u7f16\u8f91\u6bcf\u4e00\u6b21\u7531 API \u751f\u6210\u7684\u7ffb\u8bd1\u6587\u672c\u3002</p><p>\u6bcf\u4e2a\u8bcd\u6761\u7684\u7ffb\u8bd1\u6587\u672c\u4ec5\u5c55\u793a\u4e00\u79d2\u65f6\u95f4\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ToggleButton_AutoTranslateWithAPI.setText(QCoreApplication.translate("Form", u"\u81ea\u52a8\u7ffb\u8bd1", None))
#if QT_CONFIG(tooltip)
        self.PushButton_SaveProject.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u6b64\u4e3a\u4fdd\u5b58\u9879\u76ee\uff0c\u800c\u5e76\u975e\u5bfc\u51fa\u9879\u76ee\u7ffb\u8bd1\u6587\u672c\u3002</p><p>\u5982\u679c\u7ffb\u8bd1\u5df2\u7ecf\u7ed3\u675f\u5e76\u9700\u8981\u5bfc\u51fa\u53ef\u4f7f\u7528\u7684\u7ffb\u8bd1\u6587\u672c\uff0c\u8bf7\u67e5\u770b\u53f3\u4e0a\u89d2\u7684\u4e0b\u62c9\u6309\u94ae\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PushButton_SaveProject.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u672c\u9879\u76ee", None))
#if QT_CONFIG(tooltip)
        self.PushButton_ViewProject.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u9879\u76ee\u7684\u4fe1\u606f\u548c\u6570\u636e\u4ec5\u5728\u672c\u5730\u5b58\u50a8\uff0c\u5e76\u4e14\u4e0d\u80fd\u4fdd\u8bc1\u51c6\u786e\u53ef\u9760\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PushButton_ViewProject.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u672c\u9879\u76ee\u7684\u4fe1\u606f\u548c\u6570\u636e", None))
        self.CaptionLabel.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u672c\u7ffb\u8bd1\u5de5\u5177\u4ec5\u5177\u5907\u8c03\u7528\u5916\u90e8 API \u8fdb\u884c\u7ffb\u8bd1\u7684\u80fd\u529b\uff1b\u4efb\u4f55\u5916\u90e8\u7ffb\u8bd1 API \u5747\u4e0e\u672c\u5de5\u5177\u65e0\u4efb\u4f55\u5173\u7cfb\u3002<br/>\u672c\u5de5\u5177\u65e0\u6cd5\u4fdd\u8bc1\u5916\u90e8 API \u8c03\u7528\u6240\u5f97\u7ffb\u8bd1\u7ed3\u679c\u7684\u51c6\u786e\u6027\u4e0e\u53ef\u9760\u6027\u3002</p></body></html>", None))
    # retranslateUi

