# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TranslateCreateProject.ui'
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
from qfluentwidgets import CardWidget
from qfluentwidgets import SimpleCardWidget
from qfluentwidgets import SmoothScrollArea
from qfluentwidgets import PopUpAniStackedWidget
from qfluentwidgets import BodyLabel
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import LineEdit
from qfluentwidgets import PlainTextEdit


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(696, 474)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 42, -1, -1)
        self.SmoothScrollArea = SmoothScrollArea(Form)
        self.SmoothScrollArea.setObjectName(u"SmoothScrollArea")
        self.SmoothScrollArea.setMinimumSize(QSize(0, 100))
        self.SmoothScrollArea.setMaximumSize(QSize(16777215, 100))
        self.SmoothScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 676, 98))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.SimpleCardWidget_Json = SimpleCardWidget(self.scrollAreaWidgetContents)
        self.SimpleCardWidget_Json.setObjectName(u"SimpleCardWidget_Json")
        self.verticalLayout_2 = QVBoxLayout(self.SimpleCardWidget_Json)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SubtitleLabel = SubtitleLabel(self.SimpleCardWidget_Json)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")

        self.verticalLayout_2.addWidget(self.SubtitleLabel)

        self.BodyLabel = BodyLabel(self.SimpleCardWidget_Json)
        self.BodyLabel.setObjectName(u"BodyLabel")

        self.verticalLayout_2.addWidget(self.BodyLabel)


        self.horizontalLayout.addWidget(self.SimpleCardWidget_Json)

        self.SimpleCardWidget_Copy = SimpleCardWidget(self.scrollAreaWidgetContents)
        self.SimpleCardWidget_Copy.setObjectName(u"SimpleCardWidget_Copy")
        self.verticalLayout_3 = QVBoxLayout(self.SimpleCardWidget_Copy)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.SubtitleLabel_2 = SubtitleLabel(self.SimpleCardWidget_Copy)
        self.SubtitleLabel_2.setObjectName(u"SubtitleLabel_2")

        self.verticalLayout_3.addWidget(self.SubtitleLabel_2)

        self.BodyLabel_2 = BodyLabel(self.SimpleCardWidget_Copy)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")

        self.verticalLayout_3.addWidget(self.BodyLabel_2)


        self.horizontalLayout.addWidget(self.SimpleCardWidget_Copy)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.SmoothScrollArea)

        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName(u"PopUpAniStackedWidget")
        self.page_Json = QWidget()
        self.page_Json.setObjectName(u"page_Json")
        self.verticalLayout_5 = QVBoxLayout(self.page_Json)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.BodyLabel_Json = BodyLabel(self.page_Json)
        self.BodyLabel_Json.setObjectName(u"BodyLabel_Json")

        self.verticalLayout_5.addWidget(self.BodyLabel_Json)

        self.PlainTextEdit_Json_Example = PlainTextEdit(self.page_Json)
        self.PlainTextEdit_Json_Example.setObjectName(u"PlainTextEdit_Json_Example")
        self.PlainTextEdit_Json_Example.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.PlainTextEdit_Json_Example)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.LineEdit_Json_ImportFile = LineEdit(self.page_Json)
        self.LineEdit_Json_ImportFile.setObjectName(u"LineEdit_Json_ImportFile")
        self.LineEdit_Json_ImportFile.setMinimumSize(QSize(0, 30))
        self.LineEdit_Json_ImportFile.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_2.addWidget(self.LineEdit_Json_ImportFile)

        self.PushButton_Json_ImportFile = PushButton(self.page_Json)
        self.PushButton_Json_ImportFile.setObjectName(u"PushButton_Json_ImportFile")
        self.PushButton_Json_ImportFile.setMinimumSize(QSize(0, 30))
        self.PushButton_Json_ImportFile.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_2.addWidget(self.PushButton_Json_ImportFile)

        self.PrimaryPushButton_Json_Create = PrimaryPushButton(self.page_Json)
        self.PrimaryPushButton_Json_Create.setObjectName(u"PrimaryPushButton_Json_Create")
        self.PrimaryPushButton_Json_Create.setMinimumSize(QSize(0, 30))
        self.PrimaryPushButton_Json_Create.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_2.addWidget(self.PrimaryPushButton_Json_Create)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.PopUpAniStackedWidget.addWidget(self.page_Json)
        self.page_Copy = QWidget()
        self.page_Copy.setObjectName(u"page_Copy")
        self.PopUpAniStackedWidget.addWidget(self.page_Copy)

        self.verticalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        self.PopUpAniStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SubtitleLabel.setText(QCoreApplication.translate("Form", u"Json\u683c\u5f0f", None))
        self.BodyLabel.setText(QCoreApplication.translate("Form", u"\u4f8b\u5982 Minecraft \u8d44\u6e90\u5305\u4e2d\u7684\u591a\u8bed\u8a00\u6587\u4ef6\u683c\u5f0f", None))
        self.SubtitleLabel_2.setText(QCoreApplication.translate("Form", u"\u4ece\u5df2\u6709\u9879\u76ee\u590d\u5236", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("Form", u"\u590d\u5236\u4e00\u4e2a\u5df2\u6709\u7684\u7ffb\u8bd1\u5de5\u7a0b\u9879\u76ee\u7684\u6e90\u6587\u672c\u4f5c\u4e3a\u65b0\u9879\u76ee", None))
        self.BodyLabel_Json.setText(QCoreApplication.translate("Form", u"\u652f\u6301\u4e0b\u65b9\u683c\u5f0f\u7684Json\u6587\u4ef6\uff0c\u8bf7\u6ce8\u610f\u7ffb\u8bd1\u5de5\u5177\u4e0d\u4f1a\u4fdd\u7559\u952e\u540d\uff0c\u53ea\u4f1a\u4fdd\u7559\u952e\u503c\u4ee5\u8fdb\u884c\u7ffb\u8bd1\u3002", None))
        self.LineEdit_Json_ImportFile.setPlaceholderText("")
        self.PushButton_Json_ImportFile.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165", None))
        self.PrimaryPushButton_Json_Create.setText(QCoreApplication.translate("Form", u"\u786e\u8ba4", None))
    # retranslateUi

