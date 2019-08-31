#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

from utils import *
from chinese_cut import *
from actions import *
from chinese import *
from owlready2 import *

from error import *


PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")
gimbiseo.metadata.comment.append("Human-Machine Dialogue System")

def print_(something, prompt='--', *args, **kwargs):
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

def main(memory):
    with gimbiseo:
        
        while True:
            q = input('-- ')
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
                    print_(memory.no_repeat)
                    continue
                else:
                    memory.record(q)
                    try:
                        ans = p(memory)
                        if ans:
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
                    print(ans)
                else:
                    print(memory.unknown)
            elif isinstance(p, GeneralQuestionAction):
                ans = answer(p, memory)
                if ans:
                    print(memory.yes)
                else:
                    print(memory.no)
            else:
                print_(memory.excuse)

if __name__ == '__main__':
    main(memory)
