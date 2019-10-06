#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import logging
jieba.setLogLevel(logging.INFO)

jieba.add_word('是一种', 100, tag='')
# jieba.add_word('不', 100000000, tag='')

keywords={'是':':', '是一种':'<:', '的':'的', '吗':'ma', '？':'?'}
keywords={'是':'是', '的':'的', '吗':'ma', '？':'？', '什么':'什么', '哪个':'哪个', '只':'q:只'}

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
            k += 1
            while True:
                nz.append(words_[k].word)
                k += 1
                if words_[k].word == '"':
                    break
            words.append(f'''"{''.join(nz)}"''')
            jieba.add_word(''.join(nz), 100, tag='ind')
        elif words_[k].word == '[':
            t = []
            k += 1
            if words_[k].flag in {'x', 'eng'}:
                tag = words_[k].word
                k += 1
            else:
                tag = None
            while True:
                t.append(words_[k].word)
                k += 1
                if words_[k].word == ']':
                    break
            if tag:
                tt = f"{tag}:{''.join(t)}"
                jieba.add_word(''.join(t), 100, tag=tag)
            else:
                tt = ''.join(t)
                jieba.add_word(tt, 100, tag='')
            words.append(tt)
        else:
            words.append(words_[k])
        k += 1
    return words

def join(words):
    new = []
    l = len(words)
    k=0
    while k<l-1:
        w=words[k]
        n=words[k+1]
        if not isinstance(w, str):
            ww = w.word
        else:
            ww = w
        if not isinstance(n, str):
            nw = n.word
        else:
            nw =n
        if ww =='定义' and nw=='为':
            new.append('定义为')
            k+=2
        elif ww=='是' and nw=='一种':
            new.append('是一种')
            k+=2
        else:
            new.append(w)
            k+=1
    new.append(words[-1])
    return new


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
        if w in keywords:
            return keywords[w]
        else:
            return w
    if w.word in keywords:
        return keywords[w.word]
    elif w.flag in {'uj', 'n', 'd', 'zg', 'nz'}:
        return w.word
    elif w.flag in {'nr', 'ns', 'nrt', 'nt', 'r', 'm', 'ind'}:
        return f'"{w.word}"'
    else:
        if w.flag:
            return f'{w.flag}:{w.word}'
        else:
            return w.word


def cut_flag(s, convert=convert):
    words = join(cut_(s))
    return ' '.join(map(convert, words))

# print(cut_flag('我不是一种社会'))
