#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

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
    from qadict import test1, test2, test3, test4
    q_as = test4
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
                assert a == '' or memory.excuse == a
                print_(memory.excuse)
                continue
            if isinstance(p, StatementAction):
                if q in memory.history:
                    assert a == '' or memory.no_repeat == a
                    print_(memory.no_repeat)
                    continue
                else:
                    memory.record(q)
                    try:
                        ans = p(memory)
                        if ans:
                            assert a == '' or memory.get == a
                            print_(memory.get)
                            memory.re_exec()
                    except NameError as e:
                        print_(e)
                        memory.cache(p)
                    except Exception as e:
                        print_(memory.excuse)
            elif isinstance(p, GeneralQuestionAction):
                try:
                    ans = answer(p, memory)
                    if ans:
                        assert a == '' or memory.yes == a
                        print(memory.yes)
                    else:
                        assert a == '' or memory.no == a
                        print(memory.no)
                except Exception as e:
                    print(e)
            elif isinstance(p, SpecialQuestionAction):
                try:
                    ans = answer(p, memory)
                    if ans:
                        assert a == '' or ans == a
                        print(ans)
                    else:
                        print(memory.unknown)
                except Exception as e:
                    print(e)
            else:
                print_(memory.excuse)

if __name__ == '__main__':
    main(memory)

