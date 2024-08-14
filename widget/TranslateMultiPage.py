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

from qfluentwidgets import PushButton
from qfluentwidgets import SplitPushButton
from qfluentwidgets import PrimarySplitPushButton
from qfluentwidgets import ToolButton
from qfluentwidgets import SingleDirectionScrollArea
from qfluentwidgets import BodyLabel
from qfluentwidgets import SubtitleLabel


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1144, 576)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 924, 489))
        self.SingleDirectionScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.SingleDirectionScrollArea)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PushButton_SaveProject = PushButton(Form)
        self.PushButton_SaveProject.setObjectName(u"PushButton_SaveProject")

        self.verticalLayout.addWidget(self.PushButton_SaveProject)

        self.PrimarySplitPushButton_TranslateWithAPI = PrimarySplitPushButton(Form)
        self.PrimarySplitPushButton_TranslateWithAPI.setObjectName(u"PrimarySplitPushButton_TranslateWithAPI")

        self.verticalLayout.addWidget(self.PrimarySplitPushButton_TranslateWithAPI)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.PushButton_PageBefore = PushButton(Form)
        self.PushButton_PageBefore.setObjectName(u"PushButton_PageBefore")

        self.horizontalLayout_3.addWidget(self.PushButton_PageBefore)

        self.PushButton_PageAfter = PushButton(Form)
        self.PushButton_PageAfter.setObjectName(u"PushButton_PageAfter")

        self.horizontalLayout_3.addWidget(self.PushButton_PageAfter)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

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
        self.PrimarySplitPushButton_TranslateWithAPI.setProperty("text_", QCoreApplication.translate("Form", u"\u6279\u91cf\u8c03\u7528API\u6267\u884c\u7ffb\u8bd1", None))
        self.PushButton_PageBefore.setText(QCoreApplication.translate("Form", u"<<<", None))
        self.PushButton_PageAfter.setText(QCoreApplication.translate("Form", u">>>", None))
        self.BodyLabel.setText(QCoreApplication.translate("Form", u"Body label", None))
    # retranslateUi

