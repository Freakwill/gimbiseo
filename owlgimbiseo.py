#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

import sh
from owlready2 import *

import english, chinese


PATH = pathlib.Path("kb")
onto_path.append(PATH)
gimbiseo = get_ontology("http://test.org/gimbiseo.owl")

language = chinese  # or english

class Person(Thing):
    pass

def parse(s):
    return language.toLogic(s)

def print_say(something, prompt='--'):
    print(prompt, something)
    # sh.say(something)

template = {'whatis': 'What is %s?', 'yes': 'Yes', 'no': 'No', 'get': 'I get', 'unknown': 'I don\'t know', 'think': 'I am thinking...'} 
template = {'whatis': '%s是什么?', 'yes': '是', 'no': '不是', 'get': '我知道了', 'unknown': '我不知道', 'think': '让我想一想'}

def answer(q, memory):
    print_say(template['think'])
    sync_reasoner(debug=0)
    return q.exec(memory)

def ask(q, memory):
    if q.first not in memory:
        print_say(template['whatis'] % (q.first))
    elif q.second not in memory:
        print_say(template['whatis'] % (q.second))
    elif q.relation not in memory and (q.relation != 'isa' and q.relation != '是'):
        print_say(template['whatis'] % (q.relation))

_dict = {'事物': 'Thing', '东西': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
 '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}

class Memory(dict):
    _template = template

    def __getitem__(self, k):
        if super(Memory, self).__contains__(k):
            return super(Memory, self).__getitem__(k)
        elif k in _dict:
            return super(Memory, self).__getitem__(_dict[k])
        else:
            print(self._template['whatis'] %k)
            

    def __contains__(self, k):
        return k in _dict or super(Memory, self).__contains__(k)

    @property
    def template(self):
        return self._template
    
memory = Memory(locals().copy())

with gimbiseo:
    while True:
        q = input('-- ')
        # sh.say(q)
        q = parse(q)
        if isinstance(q, language.StatementAction):
            a = q.exec(memory)
            if a:
                print_say(template['get'])
        elif isinstance(q, language.GeneralQuestionAction):
            try:
                a = answer(q, memory)
                if a:
                    print_say(template['yes'])
                else:
                    print_say(template['no'])
            except Exception:
                ask(q, memory)
        else:
            try:
                a = answer(q, memory)
                if a:
                    print_say(a)
                else:
                    print_say(template['unknown'])
            except Exception:
                ask(q, memory)

# gimbiseo.save()
