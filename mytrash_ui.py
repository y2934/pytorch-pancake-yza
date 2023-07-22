# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mytrash.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(704, 569)
        MainWindow.setStyleSheet(u"background-color: rgb(39, 44, 54);\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background: transparent;\n"
"font: 25 15pt \"\u5fae\u8f6f\u96c5\u9ed1 Light\";\n"
"color: rgb(235, 235, 235);\n"
"\n"
"")

        self.verticalLayout.addWidget(self.label)

        self.plainTextEdit_2 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_2.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_2.setSizePolicy(sizePolicy)
        self.plainTextEdit_2.setMinimumSize(QSize(200, 200))
        self.plainTextEdit_2.setStyleSheet(u"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(213, 213, 213);\n"
"	font: 75 13pt \"\u7b49\u7ebf\";\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"}\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.plainTextEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setTabStopWidth(80)
        #self.plainTextEdit_2.setTabStopDistance(80.000000000000000)
        self.plainTextEdit_2.setCursorWidth(0)
        self.plainTextEdit_2.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.plainTextEdit_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"background: transparent;\n"
"font: 25 15pt \"\u5fae\u8f6f\u96c5\u9ed1 Light\";\n"
"color: rgb(235, 235, 235);\n"
"\n"
"")

        self.verticalLayout_2.addWidget(self.label_2)

        self.plainTextEdit_3 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")
        self.plainTextEdit_3.setMinimumSize(QSize(200, 200))
        self.plainTextEdit_3.setStyleSheet(u"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"}\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.plainTextEdit_3.setInputMethodHints(Qt.ImhMultiLine)
        self.plainTextEdit_3.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.plainTextEdit_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(0, 91))
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"	\n"
"	color: rgb(213, 213, 213);\n"
"	font: 75 15pt \"\u7b49\u7ebf\";\n"
"	\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:rgb(33, 37, 43);\n"
"	\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color:rgb(0, 84, 252);\n"
"	\n"
"}")
        self.pushButton_5.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.pushButton_5)

        self.horizontalSpacer = QSpacerItem(20, 14, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 91))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"	\n"
"	color: rgb(213, 213, 213);\n"
"	font: 75 15pt \"\u7b49\u7ebf\";\n"
"	\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:rgb(33, 37, 43);\n"
"	\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color:rgb(0, 84, 252);\n"
"	\n"
"}")
        self.pushButton_2.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.horizontalSpacer_2 = QSpacerItem(20, 14, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 91))
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"	\n"
"	color: rgb(213, 213, 213);\n"
"	font: 75 15pt \"\u7b49\u7ebf\";\n"
"	\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:rgb(33, 37, 43);\n"
"	\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color:rgb(0, 84, 252);\n"
"	\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.horizontalSpacer_3 = QSpacerItem(20, 14, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(0, 91))
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"	\n"
"	color: rgb(213, 213, 213);\n"
"	font: 75 15pt \"\u7b49\u7ebf\";\n"
"	\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:rgb(33, 37, 43);\n"
"	\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color:rgb(0, 84, 252);\n"
"	\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 2)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 704, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u667a\u80fd\u5783\u573e\u6876", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5783\u573e\u6295\u653e\u60c5\u51b5\uff1a", None))
#if QT_CONFIG(whatsthis)
        self.plainTextEdit_2.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.plainTextEdit_2.setPlainText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6ea2\u6ee1\u60c5\u51b5\uff1a", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u5f00  \u59cb", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u505c  \u6b62", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u91cd  \u542f", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u64ad  \u653e", None))
    # retranslateUi

