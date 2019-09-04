#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import time, random

from utils import *
from chinese_cut import *
from actions import *
from chinese import *
from owlready2 import *

from error import *

print('人机对话5秒钟后开始', end='')
for _ in range(5):
    time.sleep(1)
    print('.', end='')
print('\n\n')

PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")
gimbiseo.metadata.comment.append("Human-Machine Dialogue System")

def print1(something, prompt='User: ',*args, **kwargs):
    print(prompt, end=' ')
    for s in something:
        print(s, end='')
        time.sleep(random.random())
    print()

def print_(something, prompt='AI: ',*args, **kwargs):
    print(prompt, something, *args, **kwargs)


def answer(q, memory):
    # close_world(gimbiseo)
    print_(memory.template['think'], end='...')
    try:
        sync_reasoner(debug=0)
    except Exception as ex:
        print(ex, end='')
    return q.exec(memory)

memory = ChineseMemory()

from qadict import *

def main(memory):
    
    q_as = test6
    with gimbiseo:
        for q, a in q_as.items():
            # sh.say(q)
            print1(q)
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
                # assert a == '' or memory.excuse == a
                print_(memory.excuse)
                continue
            if isinstance(p, StatementAction):
                if q in memory.history:
                    assert a == '' or memory.no_repeat == a, AnswerError(memory.no_repeat, a)
                    print_(memory.no_repeat)
                    continue
                else:
                    memory.record(q)
                    try:
                        ans = p(memory)
                        if ans:
                            assert a == '' or memory.get == a, AnswerError(memory.get, a)
                            print_(memory.get)
                            memory.re_exec()
                    except NameError as e:
                        print_(e)
                        memory.cache(p)
                    except Exception as e:
                        print_(memory.excuse)
            elif isinstance(p, SpecialQuestionAction):
                ans = answer(p, memory)
                if ans:
                    assert a == '' or ans == a, AnswerError(ans, a)
                    print(ans)
                else:
                    print(memory.unknown)
            elif isinstance(p, GeneralQuestionAction):
                ans = answer(p, memory)
                if ans:
                    assert a == '' or memory.yes == a, AnswerError(memory.yes, a)
                    print(memory.yes)
                else:
                    assert a == '' or memory.no == a, AnswerError(memory.no, a)
                    print(memory.no)
            else:
                print_(memory.excuse)

if __name__ == '__main__':
    main(memory)

