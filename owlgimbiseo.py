#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sh

from gimbiseo import *
from owlready2 import *

PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")
gimbiseo.metadata.comment.append("Human-Machine Dialogue System")

language = chinese  # or english

def parse(s):
    return language.toLogic(s)

def print_say(something, prompt='--',*args, **kwargs):
    print(prompt, something, *args, **kwargs)
    # sh.say(something)

def answer(q, memory):
    close_world(gimbiseo)
    print_say(memory.template['think'], end='...')
    sync_reasoner(debug=0)
    return q(memory)


class ChineseMemory(Memory):
    _template = {'whatis': '%s是什么?', 'yes': '是', 'no': '不是', 'get': '我知道了', 'unknown': '我不知道', 'think': '让我想一想', 'excuse':'能再说一遍吗？'}
    _dict = {'事物': 'Thing', '东西': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
    '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}

memory = ChineseMemory()

def main():
    with gimbiseo:
        memory = ChineseMemory()
        while True:
            # sh.say(q)
            try:
                q = input('-- ')
                q = parse(q)
            except:
                print_say(memory.excuse)
                continue
            if isinstance(q, language.StatementAction):
                try:
                    a = q(memory)
                    if a:
                        print_say(memory.get)
                except:
                    print_say(memory.excuse)
            elif isinstance(q, language.GeneralQuestionAction):
                try:
                    a = answer(q, memory)
                    if a:
                        print_say(memory.yes)
                    else:
                        print_say(memory.no)
                except Exception as e:
                    print(e)
            elif isinstance(q, language.SpecialQuestionAction):
                try:
                    a = answer(q, memory)
                    if a:
                        print_say(a)
                    else:
                        print_say(memory.unknown)
                except Exception:
                    q(memory)
            else:
                print_say(memory.excuse)

    # gimbiseo.save()

if __name__ == '__main__':
    main()

