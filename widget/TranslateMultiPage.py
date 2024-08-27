# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TranslateMultiPage.ui'
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
from qfluentwidgets import SingleDirectionScrollArea
from qfluentwidgets import CaptionLabel
from qfluentwidgets import BodyLabel
from qfluentwidgets import SubtitleLabel


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1144, 679)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 42, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.SubtitleLabel = SubtitleLabel(Form)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")

        self.horizontalLayout.addWidget(self.SubtitleLabel)

        self.SplitPushButton = SplitPushButton(Form)
        self.SplitPushButton.setObjectName(u"SplitPushButton")

        self.horizontalLayout.addWidget(self.SplitPushButton)

        self.ToolButton_Guide = ToolButton(Form)
        self.ToolButton_Guide.setObjectName(u"ToolButton_Guide")

        self.horizontalLayout.addWidget(self.ToolButton_Guide)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.SingleDirectionScrollArea = SingleDirectionScrollArea(Form)
        self.SingleDirectionScrollArea.setObjectName(u"SingleDirectionScrollArea")
        self.SingleDirectionScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 924, 561))
        self.SingleDirectionScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.SingleDirectionScrollArea)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PushButton_SaveProject = PushButton(Form)
        self.PushButton_SaveProject.setObjectName(u"PushButton_SaveProject")

        self.verticalLayout.addWidget(self.PushButton_SaveProject)

        self.PushButton_Glossary = PushButton(Form)
        self.PushButton_Glossary.setObjectName(u"PushButton_Glossary")
        self.PushButton_Glossary.setTabletTracking(False)

        self.verticalLayout.addWidget(self.PushButton_Glossary)

        self.ComboBox_API = ComboBox(Form)
        self.ComboBox_API.setObjectName(u"ComboBox_API")

        self.verticalLayout.addWidget(self.ComboBox_API)

        self.PrimaryPushButton_TranslateWithAPI = PrimaryPushButton(Form)
        self.PrimaryPushButton_TranslateWithAPI.setObjectName(u"PrimaryPushButton_TranslateWithAPI")

        self.verticalLayout.addWidget(self.PrimaryPushButton_TranslateWithAPI)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.PushButton_PageBefore = PushButton(Form)
        self.PushButton_PageBefore.setObjectName(u"PushButton_PageBefore")

        self.horizontalLayout_3.addWidget(self.PushButton_PageBefore)

        self.PushButton_PageAfter = PushButton(Form)
        self.PushButton_PageAfter.setObjectName(u"PushButton_PageAfter")

        self.horizontalLayout_3.addWidget(self.PushButton_PageAfter)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.CaptionLabel = CaptionLabel(Form)
        self.CaptionLabel.setObjectName(u"CaptionLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CaptionLabel.sizePolicy().hasHeightForWidth())
        self.CaptionLabel.setSizePolicy(sizePolicy)
        self.CaptionLabel.setMaximumSize(QSize(190, 16777215))
        self.CaptionLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.CaptionLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.BodyLabel = BodyLabel(Form)
        self.BodyLabel.setObjectName(u"BodyLabel")

        self.verticalLayout_2.addWidget(self.BodyLabel)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SubtitleLabel.setText(QCoreApplication.translate("Form", u"Subtitle label", None))
        self.SplitPushButton.setProperty("text_", QCoreApplication.translate("Form", u"\u4e0b\u62c9\u9009\u62e9\u5feb\u901f\u64cd\u4f5c\u7c7b\u578b", None))
        self.PushButton_SaveProject.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u9879\u76ee", None))
        self.PushButton_Glossary.setText(QCoreApplication.translate("Form", u"\u672f\u8bed\u8868", None))
        self.ComboBox_API.setText(QCoreApplication.translate("Form", u"\u9009\u62e9API\u4ee5\u4f9b\u8c03\u7528", None))
        self.PrimaryPushButton_TranslateWithAPI.setText(QCoreApplication.translate("Form", u"\u6279\u91cf\u8c03\u7528API\u6267\u884c\u7ffb\u8bd1", None))
        self.PushButton_PageBefore.setText(QCoreApplication.translate("Form", u"<<<", None))
        self.PushButton_PageAfter.setText(QCoreApplication.translate("Form", u">>>", None))
        self.CaptionLabel.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u672c\u9875\u9762\u662f\u5217\u8868\u591a\u9879\u8bcd\u6761\u7ffb\u8bd1\u5668\u7684\u9875\u9762\uff0c\u9488\u5bf9\u67d0\u4e00\u8bcd\u6761\u7684\u5de5\u5177\u6309\u94ae\u5747\u653e\u7f6e\u5728\u8be5\u8bcd\u6761\u5361\u7247\u4e0a\uff0c\u6240\u6709\u8bcd\u6761\u5728\u53d1\u751f\u53d8\u5316\u4e4b\u540e\u90fd\u4f1a\u81ea\u52a8\u4fdd\u5b58\uff0c\u4f46\u60a8\u4ecd\u7136\u9700\u8981\u624b\u52a8\u2b06\ufe0f\u4fdd\u5b58\u9879\u76ee\u2b06\ufe0f\u3002</p><p>\u60a8\u9700\u8981\u5148\u5728\u5de5\u5177\u7bb1\u8bbe\u7f6e\u4e2d\u914d\u7f6e\u7ffb\u8bd1API\u7684\u51ed\u8bc1\uff0c\u7136\u540e\u624d\u80fd\u8c03\u7528API\u8fdb\u884c\u7ffb\u8bd1\u3002\u60a8\u70b9\u51fb\u4e0a\u65b9\u8c03\u7528API\u7ffb\u8bd1\u7684\u6309\u94ae\u540e\uff0c\u672c\u9875\u7684\u6240\u6709\u672a\u63d0\u4f9b\u7ffb\u8bd1\u6587\u672c\u7684\u8bcd\u6761\u90fd\u4f1a\u88ab\u63d0\u4ea4\u7ffb\u8bd1\uff0c\u7ffb\u8bd1\u7ed3\u679c\u5c06\u81ea\u52a8\u586b\u5145\u81f3\u8bd1\u6587\u8f93\u5165\u884c\u4e2d\u3002</p><p>\u6279\u91cf\u8c03\u7528API\u7ffb"
                        "\u8bd1\u5e76\u4e0d\u80fd\u8ba9\u672c\u9875\u7684\u6240\u6709\u5185\u5bb9\u77ac\u95f4\u5b8c\u6210\u7ffb\u8bd1\uff0cAPI\u8c03\u7528\u63a5\u53e3\u4f1a\u5c4f\u853d\u8fc7\u5feb\u7684\u8bbf\u95ee\uff0c\u56e0\u6b64\u4e24\u6b21\u7ffb\u8bd1\u4e4b\u95f4\u5b58\u5728\u4e00\u79d2\u7684\u95f4\u9694\u3002</p></body></html>", None))
        self.BodyLabel.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:9pt;\">\u672c\u7ffb\u8bd1\u5de5\u5177\u4ec5\u5177\u5907\u8c03\u7528\u5916\u90e8 API \u8fdb\u884c\u7ffb\u8bd1\u7684\u80fd\u529b\uff1b\u4efb\u4f55\u5916\u90e8\u7ffb\u8bd1 API \u5747\u4e0e\u672c\u5de5\u5177\u65e0\u4efb\u4f55\u5173\u7cfb\u3002\u672c\u5de5\u5177\u65e0\u6cd5\u4fdd\u8bc1\u5916\u90e8 API \u8c03\u7528\u6240\u5f97\u7ffb\u8bd1\u7ed3\u679c\u7684\u51c6\u786e\u6027\u4e0e\u53ef\u9760\u6027\u3002</span></p></body></html>", None))
    # retranslateUi

