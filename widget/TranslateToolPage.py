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

from qfluentwidgets import PushButton
from qfluentwidgets import PrimaryPushButton
from qfluentwidgets import SplitPushButton
from qfluentwidgets import PrimarySplitPushButton
from qfluentwidgets import SplitToolButton
from qfluentwidgets import ToggleButton
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import TextEdit
from qfluentwidgets import PlainTextEdit


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(805, 510)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.SubtitleLabel = SubtitleLabel(Form)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")

        self.horizontalLayout_7.addWidget(self.SubtitleLabel)

        self.SplitToolButton = SplitToolButton(Form)
        self.SplitToolButton.setObjectName(u"SplitToolButton")

        self.horizontalLayout_7.addWidget(self.SplitToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.PlainTextEdit_OriginalText = PlainTextEdit(Form)
        self.PlainTextEdit_OriginalText.setObjectName(u"PlainTextEdit_OriginalText")
        self.PlainTextEdit_OriginalText.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.PlainTextEdit_OriginalText)

        self.PlainTextEdit_TranslatedText = PlainTextEdit(Form)
        self.PlainTextEdit_TranslatedText.setObjectName(u"PlainTextEdit_TranslatedText")

        self.horizontalLayout_2.addWidget(self.PlainTextEdit_TranslatedText)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PrimarySplitPushButton_API = PrimarySplitPushButton(Form)
        self.PrimarySplitPushButton_API.setObjectName(u"PrimarySplitPushButton_API")

        self.verticalLayout.addWidget(self.PrimarySplitPushButton_API)

        self.PushButton_EditPrompt = PushButton(Form)
        self.PushButton_EditPrompt.setObjectName(u"PushButton_EditPrompt")

        self.verticalLayout.addWidget(self.PushButton_EditPrompt)

        self.PushButton_EditAPIConfig = PushButton(Form)
        self.PushButton_EditAPIConfig.setObjectName(u"PushButton_EditAPIConfig")

        self.verticalLayout.addWidget(self.PushButton_EditAPIConfig)

        self.PrimaryPushButton_TranslateWithAPI = PrimaryPushButton(Form)
        self.PrimaryPushButton_TranslateWithAPI.setObjectName(u"PrimaryPushButton_TranslateWithAPI")

        self.verticalLayout.addWidget(self.PrimaryPushButton_TranslateWithAPI)

        self.ToggleButton_AutoTranslateWithAPI = ToggleButton(Form)
        self.ToggleButton_AutoTranslateWithAPI.setObjectName(u"ToggleButton_AutoTranslateWithAPI")

        self.verticalLayout.addWidget(self.ToggleButton_AutoTranslateWithAPI)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.TextEdit_API = TextEdit(Form)
        self.TextEdit_API.setObjectName(u"TextEdit_API")

        self.horizontalLayout_3.addWidget(self.TextEdit_API)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.PushButton_SaveProject = PushButton(Form)
        self.PushButton_SaveProject.setObjectName(u"PushButton_SaveProject")

        self.horizontalLayout_4.addWidget(self.PushButton_SaveProject)

        self.PushButton_ViewProject = PushButton(Form)
        self.PushButton_ViewProject.setObjectName(u"PushButton_ViewProject")

        self.horizontalLayout_4.addWidget(self.PushButton_ViewProject)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SubtitleLabel.setText(QCoreApplication.translate("Form", u"Subtitle label", None))
        self.PlainTextEdit_TranslatedText.setPlaceholderText(QCoreApplication.translate("Form", u"\u5728\u6b64\u5904\u8f93\u5165\u5de6\u8fb9\u8bcd\u6761\u7684\u7ffb\u8bd1\u6587\u672c\u2026\u2026", None))
        self.PushButton_OneBefore.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u6761", None))
        self.PushButton_OneNext.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u6761", None))
        self.PrimaryPushButton_SaveAndContinue.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58 - \u4e0b\u4e00\u6761", None))
        self.PrimaryPushButton_MarkAndContinue.setText(QCoreApplication.translate("Form", u"\u6807\u8bb0 - \u4e0b\u4e00\u6761", None))
        self.PrimarySplitPushButton_API.setProperty("text_", QCoreApplication.translate("Form", u"\u558a\u4eba\u5e2e\u5fd9\u7ffb\u4e00\u4e0b", None))
        self.PushButton_EditPrompt.setText(QCoreApplication.translate("Form", u"[AI\u4e13\u7528] \u7f16\u8f91 prompt", None))
        self.PushButton_EditAPIConfig.setText(QCoreApplication.translate("Form", u"API \u914d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.PrimaryPushButton_TranslateWithAPI.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5c06\u901a\u8fc7 API \u83b7\u53d6\u7684\u7ffb\u8bd1\u5e94\u7528\u5230\u8be5\u8bcd\u6761\uff0c\u8fd9\u5c06\u81ea\u52a8\u4fdd\u5b58\u8bcd\u6761\u5e76\u6dfb\u52a0\u6807\u7b7e\u3002</p><p>\u5728\u5e94\u7528\u4e4b\u524d\uff0c\u60a8\u4ecd\u7136\u53ef\u4ee5\u5728\u53f3\u4fa7\u6587\u672c\u6846\u4e2d\u7f16\u8f91 API \u83b7\u53d6\u7684\u7ffb\u8bd1\u5b57\u6bb5\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.PrimaryPushButton_TranslateWithAPI.setText(QCoreApplication.translate("Form", u"\u5e94\u7528\u6b64\u7ffb\u8bd1", None))
#if QT_CONFIG(tooltip)
        self.ToggleButton_AutoTranslateWithAPI.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u6fc0\u6d3b\u81ea\u52a8\u7ffb\u8bd1\u671f\u95f4\uff0c\u60a8\u5c06\u65e0\u6cd5\u7f16\u8f91\u6bcf\u4e00\u6b21\u7531 API \u751f\u6210\u7684\u7ffb\u8bd1\u6587\u672c\u3002</p><p>\u6bcf\u4e2a\u8bcd\u6761\u7684\u7ffb\u8bd1\u6587\u672c\u4ec5\u5c55\u793a\u4e00\u79d2\u65f6\u95f4\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ToggleButton_AutoTranslateWithAPI.setText(QCoreApplication.translate("Form", u"\u81ea\u52a8\u7ffb\u8bd1", None))
        self.PushButton_SaveProject.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u672c\u9879\u76ee", None))
        self.PushButton_ViewProject.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u672c\u9879\u76ee\u7684\u4fe1\u606f\u548c\u6570\u636e", None))
    # retranslateUi

