# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Programming/Qt/GimbiseoUI/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("GIMBISEO")
        MainWindow.resize(655, 647)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(10000, 10000))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_logo_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_logo_2.setMinimumSize(QtCore.QSize(40, 30))
        self.label_logo_2.setMaximumSize(QtCore.QSize(91, 71))
        self.label_logo_2.setText("")
        self.label_logo_2.setObjectName("label_logo_2")
        self.gridLayout.addWidget(self.label_logo_2, 0, 0, 1, 1)
        self.label_hm = QtWidgets.QLabel(self.centralwidget)
        self.label_hm.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_hm.setFont(font)
        self.label_hm.setTextFormat(QtCore.Qt.RichText)
        self.label_hm.setScaledContents(True)
        self.label_hm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hm.setObjectName("label_hm")
        self.gridLayout.addWidget(self.label_hm, 0, 1, 1, 1)
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setMinimumSize(QtCore.QSize(40, 40))
        self.label_logo.setMaximumSize(QtCore.QSize(91, 71))
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.gridLayout.addWidget(self.label_logo, 0, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_dialogue = QtWidgets.QTextEdit(self.centralwidget)
        self.text_dialogue.setEnabled(True)
        self.text_dialogue.setMinimumSize(QtCore.QSize(0, 0))
        self.text_dialogue.setMaximumSize(QtCore.QSize(889, 350))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.text_dialogue.setFont(font)
        self.text_dialogue.setReadOnly(True)
        self.text_dialogue.setObjectName("text_dialogue")
        self.verticalLayout.addWidget(self.text_dialogue)
        self.edit_input = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_input.setMinimumSize(QtCore.QSize(20, 30))
        self.edit_input.setMaximumSize(QtCore.QSize(889, 30))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.edit_input.setFont(font)
        self.edit_input.setObjectName("edit_input")
        self.verticalLayout.addWidget(self.edit_input)
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")
        self.button_load = QtWidgets.QPushButton(self.centralwidget)
        self.button_load.setMaximumSize(QtCore.QSize(176, 35))
        self.button_load.setObjectName("button_load")
        self.buttons.addWidget(self.button_load)
        self.button_save = QtWidgets.QPushButton(self.centralwidget)
        self.button_save.setMaximumSize(QtCore.QSize(176, 35))
        self.button_save.setObjectName("button_save")
        self.buttons.addWidget(self.button_save)
        self.button_quit = QtWidgets.QPushButton(self.centralwidget)
        self.button_quit.setMaximumSize(QtCore.QSize(177, 35))
        self.button_quit.setObjectName("button_quit")
        self.buttons.addWidget(self.button_quit)
        self.button_clear = QtWidgets.QPushButton(self.centralwidget)
        self.button_clear.setMaximumSize(QtCore.QSize(176, 35))
        self.button_clear.setObjectName("button_clear")
        self.buttons.addWidget(self.button_clear)
        self.button_demo = QtWidgets.QPushButton(self.centralwidget)
        self.button_demo.setMaximumSize(QtCore.QSize(176, 35))
        self.button_demo.setObjectName("button_demo")
        self.buttons.addWidget(self.button_demo)
        self.verticalLayout.addLayout(self.buttons)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_information = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label_information.setFont(font)
        self.label_information.setObjectName("label_information")
        self.horizontalLayout_2.addWidget(self.label_information)
        self.text_information = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_information.setEnabled(True)
        self.text_information.setMaximumSize(QtCore.QSize(824, 70))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.text_information.setFont(font)
        self.text_information.setObjectName("text_information")
        self.horizontalLayout_2.addWidget(self.text_information)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 655, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile_F = QtWidgets.QMenu(self.menubar)
        self.menuFile_F.setObjectName("menuFile_F")
        self.menuHelp_H = QtWidgets.QMenu(self.menubar)
        self.menuHelp_H.setObjectName("menuHelp_H")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_L = QtWidgets.QAction(MainWindow)
        self.actionLoad_L.setObjectName("actionLoad_L")
        self.actionDocument = QtWidgets.QAction(MainWindow)
        self.actionDocument.setObjectName("actionDocument")
        self.actionHome = QtWidgets.QAction(MainWindow)
        self.actionHome.setObjectName("actionHome")
        self.actionSave_S = QtWidgets.QAction(MainWindow)
        self.actionSave_S.setObjectName("actionSave_S")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionClose_W = QtWidgets.QAction(MainWindow)
        self.actionClose_W.setObjectName("actionClose_W")
        self.menuFile_F.addAction(self.actionLoad_L)
        self.menuFile_F.addSeparator()
        self.menuFile_F.addAction(self.actionSave_S)
        self.menuFile_F.addAction(self.actionSave_As)
        self.menuFile_F.addSeparator()
        self.menuFile_F.addAction(self.actionClose_W)
        self.menuHelp_H.addAction(self.actionDocument)
        self.menuHelp_H.addAction(self.actionHome)
        self.menubar.addAction(self.menuFile_F.menuAction())
        self.menubar.addAction(self.menuHelp_H.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GIMBISEO V1.0"))
        self.label_hm.setText(_translate("MainWindow", "* 人机对话系统 *"))
        self.text_dialogue.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.SF NS Text\';\"><br /></p></body></html>"))
        self.edit_input.setPlaceholderText(_translate("MainWindow", "输入语句或命令"))
        self.button_load.setText(_translate("MainWindow", "载入"))
        self.button_save.setText(_translate("MainWindow", "保存"))
        self.button_quit.setText(_translate("MainWindow", "退出"))
        self.button_clear.setText(_translate("MainWindow", "清屏"))
        self.button_demo.setText(_translate("MainWindow", "演示"))
        self.label_information.setText(_translate("MainWindow", "打印信息"))
        self.menuFile_F.setTitle(_translate("MainWindow", "文件(&F)"))
        self.menuHelp_H.setTitle(_translate("MainWindow", "帮助(&H)"))
        self.actionLoad_L.setText(_translate("MainWindow", "Load(&L)"))
        self.actionDocument.setText(_translate("MainWindow", "Document"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionSave_S.setText(_translate("MainWindow", "Save(&S)"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionClose_W.setText(_translate("MainWindow", "Close(&W)"))
