#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sh

from utils import *
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
    '狗 是一种 动物':'*',
    '动物 是一种 事物':'我知道了',
    '"八公" 是 狗 吗？':'是',
    '狗 是一种 什么 ？':'动物',
    '狗 喜欢 骨头':'*',
    '狗狗 我好喜欢':'能再说一遍吗？',
    '骨头 是一种 事物':'我知道了',
    '狗 喜欢 骨头':'不要重复',
    '狗 喜欢 骨头 吗？':'是',
    '"八公" 喜欢 骨头 吗？':'是',
    '"八公" 是 喜欢 骨头 的 狗 吗？':'是',
    '骨头 喜欢 骨头 吗？':'不是',
    '狗 喜欢 什么 ？':'骨头',
    # '喜欢 是一种 自反关系',
    # '"八公" 喜欢 什么？'
    # '"月球" 是 卫星',
    # '卫星 是一种 天体',
    # '"地球" 是 行星',
    # '"地球" 是 行星',
    # '行星 是一种 天体',
    # '天体 是一种 事物',
    # '"太阳" 是 恒星',
    # '恒星 是一种 天体',
    # '行星 围绕 恒星',
    # '"地球" 围绕 "太阳"',
    # '"毗邻星" 是 恒星',
    # '"木卫一" 是 卫星',
    # '"木卫一" 是 卫星 吗？',
    # '"木卫一" 围绕 "木星"',
    # '"地球" 围绕 什么 ？',
    # '"木星" 是 行星',
    # '"地球" 围绕 哪个 恒星 ？',
    # '哪个 卫星 围绕 "木星"？',
    # '"地球" 不围绕 "太阳" 吗？'
    }
    with gimbiseo:
        for q, a in q_as.items():
            # sh.say(q)
            print_(q)
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

