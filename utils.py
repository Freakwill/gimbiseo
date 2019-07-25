#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import types


class Memory:

    _template = {'whatis': 'What is %s?', 'yes': 'Yes', 'no': 'No', 'get': 'I get', 'unknown': 'I don\'t know', 'think': 'I am thinking...'} 
    _dict = {}
    _locals = {}
    _globals = globals().copy()
    _cache = []
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

    def __iter__(self):
        return iter(self._locals.items())

    @property
    def template(self):
        return self._template

    @property
    def history(self):
        return self._history
    

    def __getattr__(self, p):
        return self._template[p]

    def record(self, s):
        self._history.append(s)

    def cache(self, s):
        self._cache.append(s)

    def re_exec(self):
        flag = True
        while flag:
            H = copy.deepcopy(self._cache)
            for h in H:
                try:
                    a = h(self)
                    if a:
                        self._cache.remove(h)
                        flag = True
                except:
                    pass
            else:
                flag = False

    def create(self, name, bases=()):
        if isinstance(bases, tuple):
            bases = (bases,)
        x = types.new_class(name, bases)
        self[name]=x
        return x

    def new_concept(self, *args, **kwargs):
        return create(self, *args, **kwargs)

    def new_ind(self, name, klass=object):
        x = klass(name)
        self[name]=x
        return x

commands = {'print': print}

class Command(object):
    '''Command class

    name: name of the command
    function: function of the command
    '''
    def __init__(self, name):
        self.name = name
        if name in globals():
            self.function = globals()[name]
        elif name in commands:
            self.function = commands[name]
        else:
            raise Excption('No such command')

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)

from owlready2 import *

def is_instance_of(i, c):
    # i: Thing
    if isinstance(c, And):
        return all(is_instance_of(i, cc) for cc in c.Classes)
    return c in i.is_instance_of or any(is_a(y, c) for y in i.INDIRECT_is_instance_of if hasattr(y, 'is_a'))

def is_a(x, c):
    if isinstance(c, And):
        return all(is_a(i, cc) for cc in c.Classes)
    return c in x.is_a or any(is_a(y, c) for y in x.is_a if hasattr(y, 'is_a'))

def proper(As):
    for k, A in enumerate(As):
        A = As.pop(0)
        if not any(is_a(B, A) or B==A for B in As if hasattr(B,'is_a')):
            As.append(A)
    return As

