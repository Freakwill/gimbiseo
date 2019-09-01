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
    _inds = {}
    _clss = {}
    _props = {}

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
        if k not in self._dict:
            return k in self._globals or k in self._locals
        else:
            return self._dict[k] in self._globals or self._dict[k] in self._locals

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
            H = copy.copy(self._cache)
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

    @property
    def inds(self):
        return set(a for k, a in self if isinstance(a, Thing))

    @property
    def clss(self):
        return set(a for k, a in self if isinstance(a, ThingClass))

    @property
    def props(self):
        return set(a for k, a in self if isinstance(a, ObjectPropertyClass))

    


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

def is_instance_of(i, c, exclude=set()):
    # i: Thing, c: Concept/Class
    if i.INDIRECT_is_instance_of and c in i.INDIRECT_is_instance_of:
        return True
    if isinstance(c, And):
        return all(is_instance_of(i, cc, exclude) for cc in c.Classes)
    elif isinstance(c, Or):
        return any(is_instance_of(i, cc, exclude) for cc in c.Classes)
    elif isinstance(c, Not):
        return not is_instance_of(i, c, exclude)
    elif isinstance(c, OneOf):
        return all(i == x for x in c.instances)
    elif isinstance(c, Restriction):
        i_r = getattr(i, c.property.name)
        if i_r:
            if c.type == 24:
                return is_a(c.value, i_r)
            if c.type == 25:
                return is_a(i_r, c.value)
            elif c.type == 29:
                return c.value == i_r[0]
        else:
            return False
    else:
        if i.INDIRECT_is_instance_of:
            if c in i.INDIRECT_is_instance_of:
                return True
            else:
                # for y in i.INDIRECT_is_instance_of:
                #     if y not in exclude:
                #         if is_a(y, c, exclude):
                #             return True
                #         else:
                #             exclude.add(y)
                # else:
                return False
        else:
            return False


def is_a(x, c, exclude=set()):
    if x == c:
        return True
    if x.is_a and c in x.is_a:
        return True
    elif x.INDIRECT_is_a and c in x.INDIRECT_is_a:
        return True
    if isinstance(c, And):
        return all(is_a(x, cc) for cc in c.Classes)
    elif isinstance(c, (IndividualValueList, list)):
        return x in c
    if isinstance(x, Or):
        return all(is_a(cc, c) for cc in x.Classes)
    elif isinstance(x, OneOf):
        return all(is_instance_of(xi, c) for xi in x.instances)
    else:
        # for y in x.is_a:
        #     if hasattr(y, 'is_a') and y not in exclude:
        #         if is_a(y, c, exclude):
        #             return True
        #         else:
        #             exclude = exclude.add(y)
        # else:
        return False

def proper(As):
    As = list(As)
    for _ in range(len(As)):
        A = As.pop(0)
        if not any(is_a(B, A) for B in As if hasattr(B,'is_a') and hasattr(B, 'INDIRECT_is_a')):
            As.append(A)
    return As

def pretty(x):
    if hasattr(x, 'name'):
        return x.name
    elif isinstance(x, Restriction):
        if x.type in {29, 24}:
            return x.property.name + x.value.name

