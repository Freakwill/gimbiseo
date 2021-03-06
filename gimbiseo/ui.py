#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, random, types, pathlib
import yaml

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QTextCursor, QIcon, QPixmap
from PyQt5.QtCore import QBasicTimer, QDateTime

from gimbiseo.window import *
from gimbiseo.dialogue import *


GPATH = pathlib.Path(__file__).parent

VIEW_PATH = pathlib.Path('view.yaml')
if not VIEW_PATH.exists():
    VIEW_PATH = GPATH / VIEW_PATH
view = yaml.load(VIEW_PATH.read_text())
for k, v in view.items():
    globals()[k]= v

memory = ChineseMemory()


class DialogueUI(QMainWindow, Ui_MainWindow):
    """UI for Dialogue
    """
    def __init__(self, dialogue, parent=None):
        super(DialogueUI, self).__init__(parent)
        self.setupUi(self)
        self.more_setup()
        self.dialogue = dialogue

    def more_setup(self):
        qss = pathlib.Path('style.qss')
        if not qss.exists():
            qss = GPATH / qss
        self.setStyleSheet(qss.read_text())
        self.button_save.pressed.connect(self.save)
        self.button_quit.pressed.connect(self.quit)
        self.button_demo.pressed.connect(self.demo)
        self.button_load.pressed.connect(self.load)
        self.button_clear.pressed.connect(self.clear)
        self.edit_input.returnPressed.connect(self.submit)

        self.actionLoad_L.triggered.connect(self.load)
        self.actionSave_S.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.save_as)
        self.actionClose_W.triggered.connect(self.close)
        self.actionDocument.triggered.connect(self.open_document)
        self.actionHome.triggered.connect(self.open_home)

        logo = pathlib.Path('images/logo.png')
        if not logo.exists():
            logo = GPATH / logo
        self.label_logo.setPixmap(QPixmap(str(logo)))

    def load(self):
        fname, _ = QFileDialog.getOpenFileName(self, '加载知识库', str(GPATH / 'kb'), '*.owl')
        if fname:
            self.dialogue.base=get_ontology(fname).load()
            self.inform(f'加载知识库{fname}')


    def save(self):
        self.dialogue.base.save()
        self.inform('知识库存储完毕')

    def save_as(self):
        fname, _ = QFileDialog.getOpenFileName(self, '保存知识库', str(GPATH / 'kb'), '*.owl')
        self.dialogue.base.save(fname)
        self.inform('知识库存储完毕')

    def clear(self):
        self.text_dialogue.clear()

    def quit(self):
        if False:
            self.save()
        memory.reset()
        self.inform('退出对话')

    def open_document(self):
        subprocess.run(['open', GPATH / 'helpdoc.pdf'])

    def open_home(self):
        import webbrowser
        webbrowser.open("https://github.com/Freakwill/gimbiseo")

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
        self.button_demo.setText("中止")
        self.button_demo.pressed.connect(self.demo_pause)
        self.pause = self.flag = False
        if self.flag is False:
            from .qadict import testy
            self.test = iter(testy)
            self.q = self.r = None
            self.text_information.setPlainText(f'3秒钟后开始演示')
            time.sleep(3)
            self.flag = True

        self.timer = QBasicTimer()
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(180, self)
            self.inform(f'演示开始于{QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")}')

    def demo_pause(self):
        self.button_demo.pressed.connect(self.demo)
        self.button_demo.setText("演示")
        self.pause = True

    def display(self, t, p=None):
        if p is None:
            self.text_dialogue.append(f'<div><em>{t}</em></div>')
        else:
            self.text_dialogue.append(f'''<div><img src="{str(GPATH / p['path'])}" height=18 width=18 alt="{p['emoji']}"/>: 
                <span class="{p['class']}">{t}</span></div>''')

    def timerEvent(self, e):
        if self.pause:
            return
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
                self.inform(f'演示结束于{QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")}')
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

    def inform(self, s):
        self.text_information.setPlainText(s)

