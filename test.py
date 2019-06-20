#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sh

from utils import *
from actions import *
from chinese import *
from owlready2 import *


PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")
gimbiseo.metadata.comment.append("Human-Machine Dialogue System")

def print_say(something, prompt='--',*args, **kwargs):
    print(prompt, something, *args, **kwargs)
    # sh.say(something)

def answer(q, memory):
    close_world(gimbiseo)
    print_say(memory.template['think'], end='...')
    sync_reasoner(debug=0)
    return q(memory)

class ChineseMemory(Memory):
    _template = {'whatis': '%s是什么?', 'yes': '是', 'no': '不是', 'get': '我知道了',
     'unknown': '我不知道', 'think': '让我想一想', 'excuse':'能再说一遍吗？',
     'inconsistent': '与已知的不一致'}
    _dict = {'事物': 'Thing', '东西': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
    '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}
    _globals = globals().copy()

    def warning(self, s):
        return '\%s 应该是一个 %s' % s

memory = ChineseMemory()

def main(memory):
    qs = [
    '"八公" 是 狗',
    '狗 是一种 事物',
    '"八公" 是 狗 吗？',
    '狗 喜欢 骨头',
    '骨头 是一种 事物',
    '狗 喜欢 骨头',
    '狗 喜欢 骨头 吗？',
    '"八公" 喜欢 骨头 吗？',
    '骨头 喜欢 骨头 吗？',
    '狗 喜欢 什么 ？'
    ]
    with gimbiseo:
        for q in qs:
            # sh.say(q)
            try:
                # q = input('-- ')
                print_say(q)
                if q.startswith('%'):
                    cmd = q.lstrip('%').split(' ')
                    Command(cmd[0])(memory[arg] for arg in cmd[1:])
                elif q == 'quit':
                    break
                q = parse(q)
            except:
                print_say(memory.excuse)
                continue
            if isinstance(q, StatementAction):
                try:
                    a = q(memory)
                    if a:
                        print_say(memory.get)
                        for h in memory._history:
                            try:
                                a = h(memory)
                                if a:
                                    memory._history.remove(h)
                            except:
                                pass
                except NameError as e:
                    print_say(e)
                    memory.record(q)
                except Exception as e:
                    print_say(memory.excuse)
            elif isinstance(q, GeneralQuestionAction):
                try:
                    a = answer(q, memory)
                    if a:
                        print_say(memory.yes)
                    else:
                        print_say(memory.no)
                except Exception as e:
                    print(e)
            elif isinstance(q, SpecialQuestionAction):
                try:
                    a = answer(q, memory)
                    if a:
                        print_say(a)
                    else:
                        print_say(memory.unknown)
                except Exception as e:
                    q(memory)
            else:
                print_say(memory.excuse)

    # gimbiseo.save()

if __name__ == '__main__':
    main(memory)

