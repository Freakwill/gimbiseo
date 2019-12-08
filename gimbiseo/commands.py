#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# regrister your commands in _commands {name: function}

import pathlib

_commands = {'print': lambda *a: ', '.join(a),
'help': lambda:pathlib.Path('helpdoc.md').read_text()}

class Command(object):
    '''Command class

    name: name of the command
    function: function of the command
    '''
    def __init__(self, name, args=()):
        self.name = name
        if name in globals():
            self.function = globals()[name]
        elif name in _commands:
            self.function = _commands[name]
        else:
            raise Exception('No such command')

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
