# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Programming/Qt/GimbiseoUI/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class BaseUI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(558, 518)
        Dialog.setMinimumSize(QtCore.QSize(0, 30))
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 30, 441, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_dialogue = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.text_dialogue.setObjectName("text_dialogue")
        self.verticalLayout.addWidget(self.text_dialogue)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 310, 441, 111))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.edit_input.setMinimumSize(QtCore.QSize(20, 20))
        self.edit_input.setObjectName("edit_input")
        self.horizontalLayout.addWidget(self.edit_input)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.button_save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_save.setObjectName("button_save")
        self.verticalLayout_3.addWidget(self.button_save)
        self.button_quit = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_quit.setObjectName("button_quit")
        self.verticalLayout_3.addWidget(self.button_quit)
        self.button_demo = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_demo.setObjectName("button_demo")
        self.verticalLayout_3.addWidget(self.button_demo)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.label_hm = QtWidgets.QLabel(Dialog)
        self.label_hm.setGeometry(QtCore.QRect(200, 10, 161, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_hm.setFont(font)
        self.label_hm.setTextFormat(QtCore.Qt.RichText)
        self.label_hm.setScaledContents(True)
        self.label_hm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hm.setObjectName("label_hm")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(50, 430, 441, 76))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_information = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_information.setObjectName("label_information")
        self.horizontalLayout_2.addWidget(self.label_information)
        self.text_information = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.text_information.setEnabled(True)
        self.text_information.setObjectName("text_information")
        self.horizontalLayout_2.addWidget(self.text_information)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.edit_input.setPlaceholderText(_translate("Dialog", "输入语句或命令"))
        self.button_save.setText(_translate("Dialog", "保存"))
        self.button_quit.setText(_translate("Dialog", "退出"))
        self.button_demo.setText(_translate("Dialog", "演示"))
        self.label_hm.setText(_translate("Dialog", "人机对话系统"))
        self.label_information.setText(_translate("Dialog", "打印信息"))
