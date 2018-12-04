#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

from owlready2 import *

import english


PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")


def parse(s):
    return english.english2logic(s)


def answer(q, memory):
    print('I am thinking...')
    # locals().update(memory)
    sync_reasoner(debug=0)
    return q.exec(memory)


def ask(q, memory):
    if q.subject not in memory:
        print('-- What is %s?' % (q.subject))
    elif q.object not in memory:
        print('-- What is %s?' % (q.object))
    elif q.relation not in memory and q.relation != 'isa':
        print('-- What is %s?' % (q.relation))


with gimbiseo:
    memory = locals()
    while True:
        q = parse(input('-- '))
        if isinstance(q, english.StatementAction):
            q.exec(memory)
            print('-- I get.')
        elif isinstance(q, english.GeneralQuestionAction):
            try:
                a = answer(q, memory)
                if a:
                    print('-- Yes')
                else:
                    print('-- No')
            except Exception:
                ask(q, memory)
        else:
            try:
                a = answer(q, memory)
                if a:
                    print('-- %s' % str(a))
                else:
                    print('-- I don\'t know')
            except Exception:
                ask(q, memory)

# gimbiseo.save()


