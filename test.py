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

memory = ChineseMemory()

def main(memory):
    qs = [
    '"八公" 是 狗',
    '狗 是一种 动物',
    '动物 是一种 事物',
    '"八公" 是 狗 吗？',
    '狗 是一种 什么 ？',
    '狗 喜欢 骨头',
    '骨头 是一种 事物',
    '狗 喜欢 骨头',
    '狗 喜欢 骨头 吗？',
    '"八公" 喜欢 骨头 吗？',
    '骨头 喜欢 骨头 吗？',
    '狗 喜欢 什么 ？',
    '"地球" 是 天体',
    '天体 是一种 事物',
    '"太阳" 是 天体',
    '"地球" 围绕 "太阳"',
    '什么 围绕 "太阳" ？',
    '"月亮" 是 天体',
    '"地球" 围绕 "月亮" 吗？',
    '"月亮" 围绕 "地球"',
    '"月亮" 围绕 什么？'
    ]
    with gimbiseo:
        for q in qs:
            # sh.say(q)
            print(q)
            try:
                if q.startswith('%'):
                    cmd = q.lstrip('%').split(' ')
                    Command(cmd[0])(memory[arg] for arg in cmd[1:])
                elif q == 'quit':
                    break
                else:
                    q = parse(q)
            except:
                print_say(memory.excuse)
                continue
            if isinstance(q, StatementAction):
                try:
                    a = q(memory)
                    if a:
                        print_say(memory.get)
                        memory.re_exec()
                except NameError as e:
                    print_say(e)
                    memory.record(q)
                except Exception as ye:
                    print_say(memory.excuse)
            elif isinstance(q, GeneralQuestionAction):
                try:
                    a = answer(q, memory)
                    if a:
                        print(memory.yes)
                    else:
                        print(memory.no)
                except Exception as e:
                    print(e)
            elif isinstance(q, SpecialQuestionAction):
                try:
                    a = answer(q, memory)
                    if a:
                        print(a)
                    else:
                        print(memory.unknown)
                except Exception as e:
                    q(memory)
            else:
                print_say(memory.excuse)

    # gimbiseo.save()

if __name__ == '__main__':
    main(memory)

