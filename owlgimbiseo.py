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


def answer(q, memory):
    # close_world(gimbiseo)
    
    try:
        sync_reasoner(debug=0)
    except Exception as ex:
        print(ex, end='')
    return q.exec(memory)

memory = ChineseMemory()


class Dialogue:
    base = gimbiseo

    def __init__(self, user_prompt='User: ', ai_prompt='AI: '):
        self.user_prompt = user_prompt
        self.ai_prompt = ai_prompt

    def __call__(self, memory):
        with Dialogue.base:
            while True:
                q = input(Dialogue.user_prompt)
                q = cut_flag(q)
                flag = self.handle(q, memory)
                if flag == 'bk':
                    break
                elif flag == 'con':
                    continue

    def test(self, dict_, memory):
        q_as = dict_
        with Dialogue.base:
            for q, a in q_as.items():
                self.print(q, self.user_prompt)
                q = cut_flag(q)
                flag = self.handle(q, memory)
                if flag == 'bk':
                    break
                elif flag == 'con':
                    continue

    def demo(self, *args, **kwargs):
        import types, random
        def demo_print(obj, something, prompt='User: ', *args, **kwargs):
            print(prompt, end=' ')
            for s in something:
                print(s, end='')
                time.sleep(random.random()*0.8)
            print()
        self.print = types.MethodType(demo_print, self)
        for _ in range(5):
            time.sleep(1)
            print('@', end=' ')
        print()
        self.test(*args, **kwargs)

    def print(self, s, prompt, *args, **kwargs):
        print(prompt, s, *args, **kwargs)


    def handle(self, q, memory):
        try:
            if q.startswith('%'):
                cmd = q.lstrip('%').split(' ')
                Command(cmd[0])(memory[arg] for arg in cmd[1:])
            elif q == 'quit':
                Dialogue.base.save()
                return 'bk'
            elif q == 'save':
                Dialogue.base.save()
            else:
                p = parse(q)
        except:
            # assert a == '' or memory.excuse == a
            self.print(self.ai_prompt, memory.excuse)
            return 'con'
        if isinstance(p, StatementAction):
            if q in memory.history:
                self.print(self.ai_prompt, memory.no_repeat)
                return 'con'
            else:
                memory.record(q)
                try:
                    ans = p(memory)
                    if ans:
                        self.print(memory.get, self.ai_prompt)
                        memory.re_exec()
                except NameError as e:
                    print(e)
                    memory.cache(p)
                except Exception as e:
                    self.print(self.ai_prompt, memory.excuse)
        elif isinstance(p, SpecialQuestionAction):
            self.print(memory.template['think'], self.ai_prompt, end='...')
            ans = answer(p, memory)
            if ans:
                self.print(ans)
            else:
                self.print(memory.unknown)
        elif isinstance(p, GeneralQuestionAction):
            self.print(memory.template['think'], self.ai_prompt, end='...')
            ans = answer(p, memory)
            if ans:
                self.print(memory.yes)
            else:
                self.print(memory.no)
        else:
            self.print(memory.excuse, self.ai_prompt)

if __name__ == '__main__':
    from qadict import *
    q_as = testy
    d = Dialogue()
    d.demo(testy, memory)
