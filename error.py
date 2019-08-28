#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ParseError(Exception):
    pass


class AnswerError(Exception):
    def __init__(self, answer, right):
        super(AnswerError, self).__init__(f'You got {answer} but the right one is {right}')