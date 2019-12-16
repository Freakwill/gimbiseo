#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import types


class Memory:

    _template = {'whatis': 'What is %s?', 'yes': 'Yes', 'no': 'No', 'iget': 'I get', 'unknown': 'I don\'t know', 'think': 'I am thinking...'} 
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

    def get(self, k, value=None):
        if k in self:
            return self[k]
        else:
            return value

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

    def reset(self):
        self._locals = {}
        self._history = []
        self._inds = {}
        self._clss = {}
        self._props = {}

    def record(self, s):
        self._history.append(s)

    def cache(self, s):
        self._cache.append(s)

    def re_exec(self):
        # execute the sentences in cache
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

