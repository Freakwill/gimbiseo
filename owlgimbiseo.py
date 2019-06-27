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


def print_(something, prompt='--', *args, **kwargs):
    print(prompt, something, *args, **kwargs)
    # sh.say(something)

def answer(q, memory):
    close_world(gimbiseo)
    print_(memory.template['think'], end='...')
    try:
        sync_reasoner(debug=0)
    except Exception as e:
        print(e, end=' ')
    return q(memory)

memory = ChineseMemory()

def main(memory):
    with gimbiseo:
        while True:
            q = input('-- ')
            try:
                if q.startswith('%'):
                    cmd = q.lstrip('%').split(' ')
                    Command(cmd[0])(memory[arg] for arg in cmd[1:])
                elif q == 'quit':
                    break
                else:
                    p = parse(q)
            except:
                print_(memory.excuse)
                continue
            if isinstance(p, StatementAction):
                if p in memory.history:
                    print(memory.no_repeat)
                else:
                    try:
                        a = p(memory)
                        if a:
                            print_(memory.get)
                            memory.re_exec()
                        memory.record(q)
                    except NameError as e:
                        print_(e)
                        memory.cache(p)
                    except Exception as ye:
                        print_(memory.excuse)
            elif isinstance(p, GeneralQuestionAction):
                try:
                    a = answer(p, memory)
                    if a:
                        print(memory.yes)
                    else:
                        print(memory.no)
                except Exception as e:
                    print(e)
            elif isinstance(p, SpecialQuestionAction):
                try:
                    a = answer(p, memory)
                    if a:
                        print(a)
                    else:
                        print(memory.unknown)
                except Exception as e:
                    print(e)
            else:
                print_(memory.excuse)

    # gimbiseo.save()

if __name__ == '__main__':
    main(memory)
