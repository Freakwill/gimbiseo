#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, random, types

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QBasicTimer, QDateTime
from window import *

from gimbiseo import *


user_symbol = '🙂'
sys_symbol = '💻'
ai_symbol = '🤖'


class DialogueUI(QMainWindow, Ui_Dialog):
    """UI for Dialogue
    """
    def __init__(self, dialogue, parent=None):
        super(DialogueUI, self).__init__(parent)
        self.setupUi(self)
        self.button_save.pressed.connect(self.save)
        self.button_quit.pressed.connect(self.quit)
        self.button_demo.pressed.connect(self.demo)
        self.edit_input.returnPressed.connect(self.submit)
        self.dialogue = dialogue


    def save(self):
        self.dialogue.base.save()

    def quit(self):
        if False:
            self.save()
        self.close()

    def submit(self):
        q = self.edit_input.text()
        self.edit_input.clear()
        self.display(q, user_symbol)
        resp = self.dialogue.handle(q, memory)
        if resp.flag == 'bk':
            self.quit()
        elif resp.flag == '%':
            self.display(resp.content, sys_symbol)
        else:
            self.display(str(resp), ai_symbol)

    def demo(self):
        # def typing(obj, t, p):
        #     self.text_dialogue.append(f'{p}: ')
        #     for i in t:
        #         self.text_dialogue.insertPlainText(i)
        # self.display = types.MethodType(typing, self)
        from qadict import testy
        self.test = iter(testy)
        self.q = self.r = self.u = self.a = None
        self.text_information.setPlainText(f'3秒钟后开始演示')
        time.sleep(3)

        self.timer = QBasicTimer()
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(150, self)
            self.text_information.setPlainText(f'演示开始于{QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")}')

    def display(self, t, p=None):
        if p is None:
            self.text_dialogue.append(f'*{t}*')
        else:
            self.text_dialogue.append(f'{p}: {t}')

    def timerEvent(self, e):
        if self.q is None:
            try:
                q, _ = next(self.test)
                self.edit_input.setText(q)
                self.q=iter(q)
            except:
                self.timer.stop()
                self.display('演示结束')
                self.text_information.setPlainText(f'演示结束于{QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")}')
        elif self.r is None:
            if self.u is None:
                self.text_dialogue.append(f'{user_symbol}: ')
                self.u = True
            try:
                if random.random()>0.5:
                    self.i = next(self.q)
                    self.text_dialogue.insertPlainText(self.i)

            except:
                q = self.edit_input.text()
                self.edit_input.clear()
                resp = self.dialogue.handle(q, memory)
                self.r = iter(str(resp))
        else:
            if self.a is None:
                self.text_dialogue.append(f'{ai_symbol}: ')
                self.a = True
            try:
                if random.random()>0.5:
                    self.i = next(self.r)
                    self.text_dialogue.insertPlainText(self.i)
            except:
                self.q = self.r = self.u = self.a = None


if __name__ == '__main__':
    memory = ChineseMemory()
    d = Dialogue()
    with d.base:
        app = QApplication([])
        myWin=DialogueUI(d)
        myWin.show()
        app.exec_()
