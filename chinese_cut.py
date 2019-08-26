#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import logging
jieba.setLogLevel(logging.INFO)

keywords={'是':':', '是一种':'<:', '的':'的', '吗':'ma', '？':'?'}

def cut(s):
    words = cut_(s)
    return ' '.join(f'"{word_flag.word}"' if word_flag.flag in {'nr', 'ns', 'nrt', 'nt', 'm'}
    else word_flag.word for word_flag in words)

def cut_(s):
    words_ = [word for word in pseg.cut(s) if word.flag != 'x' or word.word != ' ']
    k = 0
    words = []
    while k < len(words_):
        if words_[k].word == '"':
            nz = []
            k+=1
            while True:
                nz.append(words_[k].word)
                k += 1
                if words_[k].word == '"':
                    break
            nz = f'''"{''.join(nz)}"'''
            k += 1
            words.append(nz)
        words.append(words_[k])
        k+=1
    return words


def convert1(w):
    if isinstance(w, str):
        return w
    if w.word in keywords:
        return w.word
    elif w.flag in {'uj', 'n', 'd'}:
        return w.word
    elif w.flag in {'nr', 'ns', 'nrt', 'nt', 'r', 'm'}:
        return f'"{w.word}"'
    else:
        return f'{w.word}/{w.flag}'

def convert2(w):
    if isinstance(w, str):
        return w
    if w.word in keywords:
        return w.word
    elif w.flag in {'uj', 'n', 'd'}:
        return w.word
    elif w.flag in {'nr', 'ns', 'nrt', 'nt', 'r'}:
        return f'"{w.word}"'
    else:
        return f'{w.word}/{w.flag}'

def convert(w):
    if isinstance(w, str):
        return w
    if w.word in keywords:
        return keywords[w.word]
    elif w.flag in {'uj', 'n', 'd'}:
        return w.word
    elif w.flag in {'nr', 'ns', 'nrt', 'nt', 'r', 'm'}:
        return f'"{w.word}"'
    else:
        return f'{w.flag}:{w.word}'


def cut_flag(s, convert=convert):
    words = cut_(s)
    return ' '.join(map(convert, words)).replace('是 "一种"', '<:')

print(cut_flag('"地球"是快乐的围绕"毛泽东"的星球'))
