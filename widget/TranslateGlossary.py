# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TranslateGlossary.ui'
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
from qfluentwidgets import PopUpAniStackedWidget
from qfluentwidgets import CaptionLabel
from qfluentwidgets import ListWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(625, 596)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 42, -1, -1)
        self.SimpleCardWidget = SimpleCardWidget(Form)
        self.SimpleCardWidget.setObjectName(u"SimpleCardWidget")
        self.SimpleCardWidget.setMinimumSize(QSize(200, 0))
        self.SimpleCardWidget.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.SimpleCardWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ListWidget = ListWidget(self.SimpleCardWidget)
        self.ListWidget.setObjectName(u"ListWidget")

        self.verticalLayout_2.addWidget(self.ListWidget)

        self.PrimaryPushButton_SaveAndClose = PrimaryPushButton(self.SimpleCardWidget)
        self.PrimaryPushButton_SaveAndClose.setObjectName(u"PrimaryPushButton_SaveAndClose")

        self.verticalLayout_2.addWidget(self.PrimaryPushButton_SaveAndClose)

        self.CaptionLabel = CaptionLabel(self.SimpleCardWidget)
        self.CaptionLabel.setObjectName(u"CaptionLabel")

        self.verticalLayout_2.addWidget(self.CaptionLabel)


        self.horizontalLayout.addWidget(self.SimpleCardWidget)

        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName(u"PopUpAniStackedWidget")
        self.page_Global = QWidget()
        self.page_Global.setObjectName(u"page_Global")
        self.horizontalLayout_2 = QHBoxLayout(self.page_Global)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.PopUpAniStackedWidget.addWidget(self.page_Global)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.PrimaryPushButton_SaveAndClose.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u5e76\u5173\u95ed\u7a97\u53e3", None))
        self.CaptionLabel.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">\u76f4\u63a5\u5173\u95ed\u7a97\u53e3\u89c6\u4f5c\u653e\u5f03\u4fdd\u5b58</span></p></body></html>", None))
    # retranslateUi

