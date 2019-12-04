#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from owlready2 import *

from chinese_cut import *
from actions import *
from chinese import *

from utils import *
from error import *
from commands import *


PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")
gimbiseo.metadata.comment.append("Human-Machine Dialogue System")


def answer(q, memory):
    # close_world(gimbiseo)
    AllDisjoint([c for c in memory.clss])
    try:
        sync_reasoner(debug=0)
    except Exception as ex:
        print(ex, end='')
    return q.exec(memory)


class Response(object):
    '''Response of the system

    content: content of response
    flag: control status [None]
    '''
    def __init__(self, content='', flag=None):
        self.content = content
        self.flag = flag

    def __str__(self):
        return str(self.content)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self)==other
        else:
            return str(self)==str(other)

    def __getitem__(self, k):
        return (self.content, self.flag)[k]

    def __format__(self, spec=None):
        if spec:
            return f'{spec}: {self.content}'
        else:
            return f'-- {self.content}'


class Dialogue:
    """The dialuge system
    
    Variables:
        base -- knowledge base
    """

    def __init__(self, user_prompt='User: ', ai_prompt='AI: ', base=gimbiseo):
        self.user_prompt = user_prompt
        self.ai_prompt = ai_prompt
        self.base = base

    def run(self, memory, gui=False):
        with self.base:
            while True:
                q = input(Dialogue.user_prompt)
                q = cut_flag(q)
                resp = self.handle(q, memory)
                if resp.flag == 'bk':
                    break
                elif resp.flag == 'con':
                    continue
                else:
                    self.print(resp, self.ai_prompt)

    def __call__(self, memory):
        self.run(memory)

    def test(self, dict_, memory):
        q_as = dict_
        with self.base:
            for q, a in q_as:
                self.print(q, self.user_prompt)
                resp = self.handle(q, memory)
                if resp.flag == 'bk':
                    break
                elif resp.flag == 'con':
                    continue
                else:
                    self.print(resp, self.ai_prompt)

    def demo(self, *args, **kwargs):
        import types, random
        def demo_print(obj, something, prompt='', *args, **kwargs):
            print(prompt, end=' ')
            for s in something:
                print(s, end='')
                time.sleep(random.random()*0.8)
            print('', *args, **kwargs)
        self.print = types.MethodType(demo_print, self)
        for _ in range(5):
            time.sleep(1)
            print('@', end=' ')
        print()
        self.test(*args, **kwargs)

    def print(self, s, prompt='', *args, **kwargs):
        print(prompt, s, *args, **kwargs)


    def handle(self, q, memory, gui=False):
        try:
            if q.startswith('%'):
                cmd = q.lstrip('%').split(' ')
                ret = Command(cmd[0])(*(memory.get(arg, arg) for arg in cmd[1:]))
                return Response(ret, '%')
            elif q == 'quit':
                Dialogue.base.save()
                return Response('', 'bk')
            elif q == 'save':
                Dialogue.base.save()
                return Response('', 'con')
            else:
                p = parse(q, cut=True)
        except:
            # assert a == '' or memory.excuse == a
            return Response(memory.excuse, 'con')
        if isinstance(p, StatementAction):
            if q in memory.history:
                return Response(memory.no_repeat, 'con')
            else:
                memory.record(q)
                try:
                    ans = p(memory)
                    if ans:
                        memory.re_exec()
                        return Response(memory.iget)
                    else:
                        return Response()
                except NameError as e:
                    memory.cache(p)
                    return Response(e)
                except Exception as e:
                    return Response(memory.excuse)
        elif isinstance(p, SpecialQuestionAction):
            ans = answer(p, memory)
            if ans:
                return Response(ans)
            else:
                return Response(memory.unknown)
        elif isinstance(p, GeneralQuestionAction):
            ans = answer(p, memory)
            if ans is True:
                return Response(memory.yes)
            elif ans is False:
                return Response(memory.no)
            else:
                return Response(memory.none)
        else:
            return Response(memory.excuse)


if __name__ == '__main__':
    from qadict import *
    memory = ChineseMemory()
    d = Dialogue()
    d.test(dict_=testy, memory=memory)

