#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sh

from utils import *
from chinese_cut import *
from actions import *
from chinesex import *
from owlready2 import *


PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")
gimbiseo.metadata.comment.append("Human-Machine Dialogue System")

def print_(something, prompt='--',*args, **kwargs):
    print(prompt, something, *args, **kwargs)
    # sh.say(something)

def answer(q, memory):
    close_world(gimbiseo)
    print_(memory.template['think'], end='...')
    try:
        sync_reasoner(debug=0)
    except Exception as ex:
        print(ex, end='')
    return q.exec(memory)


memory = ChineseMemory()

def main(memory):
    q_as = {
    '"八公" 是 狗':'*',
    '"八公" 是 a:忠诚的':'*',
    '忠诚的 是一种 性质':'*',
    '狗 是一种 动物':'*',
    '动物 是一种 事物':'我知道了',
    '"八公" 是 狗 吗？':'是',
    '狗 是一种 什么 ？':'动物',
    '狗 v:喜欢 骨头':'*',
    '狗狗 我好喜欢':'能再说一遍吗？',
    '骨头 是一种 事物':'我知道了',
    '狗 v:喜欢 骨头':'不要重复',
    '狗 v:喜欢 骨头 吗？':'是',
    '"八公" v:喜欢 骨头 吗？':'是',
    '"八公" 是v:喜欢 骨头 的 a:忠诚的 狗 吗？':'是',
    '骨头 v:喜欢 骨头 吗？':'不是',
    '狗 v:喜欢 什么 ？':'骨头',
    }

    # q_as = {
    # '八公 是狗':'*',
    # '八公 是忠诚的':"*",
    # '狗是一种动物':'*',
    # '动物是一种事物':'我知道了',
    # '八公 是狗吗？':'是',
    # '狗是一种什么？':'动物',
    # '狗喜欢骨头':'*',
    # '狗狗我好喜欢':'能再说一遍吗？',
    # '骨头是一种事物':'我知道了',
    # '狗喜欢骨头':'不要重复',
    # '狗喜欢骨头吗？':'是',
    # '八公 喜欢骨头吗？':'是',
    # '八公 是喜欢骨头的狗吗？':'是',
    # '骨头喜欢骨头吗？':'不是',
    # '狗喜欢什么？':'骨头',
    # }
    with gimbiseo:
        for q, a in q_as.items():
            # sh.say(q)
            print_(q)
            # q = cut_flag(q)
            try:
                if q.startswith('%'):
                    cmd = q.lstrip('%').split(' ')
                    Command(cmd[0])(memory[arg] for arg in cmd[1:])
                elif q == 'quit':
                    gimbiseo.save()
                    break
                elif q == 'save':
                    gimbiseo.save()
                else:
                    p = parse(q)
            except:
                assert memory.excuse == a
                print_(memory.excuse)
                continue
            if isinstance(p, StatementAction):
                if q in memory.history:
                    assert memory.no_repeat == a
                    print_(memory.no_repeat)
                    continue
                else:
                    memory.record(q)
                    try:
                        ans = p(memory)
                        if ans:
                            assert memory.get == a
                            print_(memory.get)
                            memory.re_exec()
                    except NameError as e:
                        print_(e)
                        memory.cache(p)
                    except Exception as ye:
                        print_(memory.excuse)
            elif isinstance(p, GeneralQuestionAction):
                try:
                    ans = answer(p, memory)
                    if ans:
                        assert memory.yes == a
                        print(memory.yes)
                    else:
                        assert memory.no == a
                        print(memory.no)
                except Exception as e:
                    print(e)
            elif isinstance(p, SpecialQuestionAction):
                try:
                    ans = answer(p, memory)
                    if ans:
                        assert ans == a
                        print(ans)
                    else:
                        print(memory.unknown)
                except Exception as e:
                    print(e)
            else:
                print_(memory.excuse)

if __name__ == '__main__':
    main(memory)

