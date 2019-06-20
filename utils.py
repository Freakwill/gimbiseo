#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba.posseg as pseg

def cut_flag(s):
    words = pseg.cut(s)
    return ' '.join(f'"{word_flag.word}/{word_flag.flag}"' if word_flag.flag in {'nr', 'ns', 'nrt', 'nt', 'r'}
    else f'{word_flag.word}/{word_flag.flag}' for word_flag in words)

def cut(s):
    words = pseg.cut(s)
    return ' '.join(f'"{word_flag.word}"' if word_flag.flag in {'nr', 'ns', 'nrt', 'nt'}
    else word_flag.word for word_flag in words)

class Memory:

    _template = {'whatis': 'What is %s?', 'yes': 'Yes', 'no': 'No', 'get': 'I get', 'unknown': 'I don\'t know', 'think': 'I am thinking...'} 
    _dict = {}
    _locals = {}
    _globals = globals().copy()
    _history = []

    def __getitem__(self, k):
        if k in self._locals:
            return self._locals[k]
        elif k in self._globals:
            return self._globals[k]
        elif k in self._dict:
            return self[self._dict[k]]
        else:
            print(self._template['whatis'] %k)

    def __setitem__(self, k, v):
        self._locals[k] = v

    def __contains__(self, k):
        return k in self._dict or k in self._globals or k in self._locals

    def update(self, *args, **kwargs):
        self._locals.update(*args, **kwargs)

    def __str__(self):
        return str(self._locals)

    @property
    def template(self):
        return self._template

    def __getattr__(self, p):
        return self._template[p]

    def record(self, s):
        self._history.append(s)


class Command(object):
    '''[Summary for Class Command]Command has 2 (principal) propteries
    name: name
    function: function'''
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)


def is_instance_of(i, c):
    return c in i.INDIRECT_is_a or any(c in y.is_a for y in i.INDIRECT_is_a if hasattr(y, 'is_a'))

def is_a(x, c):
    return c in x.is_a or any(c in y.is_a for y in x.is_a if hasattr(y, 'is_a'))

