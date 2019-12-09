#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, random, types

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QTextCursor, QIcon, QPixmap
from PyQt5.QtCore import QBasicTimer, QDateTime

from gimbiseo.window import *
from gimbiseo.dialogue import *
from gimbiseo.view import *


class DialogueUI(QMainWindow, Ui_Dialog):
    """UI for Dialogue
    """
    def __init__(self, dialogue, parent=None):
        super(DialogueUI, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(qss)
        self.button_save.pressed.connect(self.save)
        self.button_quit.pressed.connect(self.quit)
        self.button_demo.pressed.connect(self.demo)
        self.button_load.pressed.connect(self.load)
        self.button_clear.pressed.connect(self.clear)
        self.edit_input.returnPressed.connect(self.submit)
        logo = pathlib.Path('images/logo.png')
        if not logo.exists():
            logo = pathlib.Path(__file__).parent / logo
        self.label_logo.setPixmap(QPixmap(str(logo)))
        self.dialogue = dialogue

    def load(self):
        self.display('目前不支持载入功能')
        # self.dialogue.base=get_ontology("file:///home/jiba/onto/pizza_onto.owl").load()


    def save(self):
        self.dialogue.base.save()

    def clear(self):
        self.text_dialogue.clear()

    def quit(self):
        if False:
            self.save()
        self.close()

    def submit(self):
        q = self.edit_input.text()
        self.edit_input.clear()
        self.display(q, user)
        resp = self.dialogue.handle(q, memory)
        if resp.flag == 'bk':
            self.quit()
        elif resp.flag == '%':
            self.display(resp.content, sys)
        else:
            self.display(str(resp), ai)

    def demo(self):
        # def typing(obj, t, p):
        #     self.text_dialogue.append(f'{p}: ')
        #     for i in t:
        #         self.text_dialogue.insertPlainText(i)
        # self.display = types.MethodType(typing, self)
        from .qadict import testy
        self.test = iter(testy)
        self.q = self.r = None
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
            self.text_dialogue.append(f'<div><em>{t}</em></div>')
        else:
            self.text_dialogue.append(f'''<div><img src="{p['path']}" height=18 width=18 alt="{p['emoji']}"/>: 
                <span class="{p['class']}">{t}</span></div>''')

    def timerEvent(self, e):
        def _submit():
            self._q = self.edit_input.text()
            self.edit_input.clear()
            self.display(self._q, user)
        def _reply(q):
            resp = self.dialogue.handle(q, memory)
            if resp.flag == 'bk':
                self.quit()
            elif resp.flag == '%':
                self.display(resp.content, sys)
            else:
                self.display(str(resp), ai)
        if self.q is None:
            try:
                q, _ = next(self.test)
                self.q=iter(q)
            except:
                self.timer.stop()
                self.display('演示结束')
                self.text_information.setPlainText(f'演示结束于{QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")}')
        elif self.r is None:
            try:
                if random.random()>0.5:
                    self.i = next(self.q)
                    self.edit_input.setText(self.edit_input.text()+self.i)
            except:
                _submit()
                self.r = True
        else:
            _reply(self._q)
            self.r = self.q = None


# if __name__ == '__main__':
#     import sys
#     memory = ChineseMemory()
#     d = Dialogue()
#     with d.base:
#         app = QApplication(sys.argv)
#         dui=DialogueUI(d)
#         dui.show()
#         os.system("pause")
#         sys.exit(app.exec_())
