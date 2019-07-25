#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import logging
jieba.setLogLevel(logging.INFO)

keywords={'是', '是一种', '的', '吗', '？'}

def cut(s):
    words = cut_(s)
    return ' '.join(f'"{word_flag.word}"' if word_flag.flag in {'nr', 'ns', 'nrt', 'nt', 'm'}
    else word_flag.word for word_flag in words)

def cut_(s):
    words = pseg.cut(s)
    return [word for word in words if word.flag != 'x' or word.word != ' ']

def convert1(w):
    if w.flag in {'nr', 'ns', 'nrt', 'nt', 'r', 'm'}:
        return f'"{w.word}"'
    elif w.flag in {'uj', 'n', 'd'}:
        return w.word
    elif w.word in keywords:
        return w.word
    else:
        return f'{w.word}/{w.flag}'

def convert2(w):
    if w.flag in {'nr', 'ns', 'nrt', 'nt', 'r'}:
        return f'"{w.word}"'
    elif w.flag in {'uj', 'n', 'd'}:
        return w.word
    elif w.word in keywords:
        return w.word
    else:
        return f'{w.word}/{w.flag}'

def convert(w):
    if w.flag in {'nr', 'ns', 'nrt', 'nt', 'r', 'm'}:
        return f'"{w.word}"'
    elif w.flag in {'uj', 'n', 'd'}:
        return w.word
    elif w.word in keywords:
        return w.word
    else:
        return f'{w.flag}:{w.word}'


def cut_flag(s, convert=convert):
    words = cut_(s)
    return ' '.join(map(convert, words)).replace('是 "一种"', '是一种')
