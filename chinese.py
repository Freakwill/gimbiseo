#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform Chinese to Logic Expressions
"""

import types

import pyparsing as pp
import pyparsing_ext as ppx

from actions import *

_dict = {'事物': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
 '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}

class ChineseMemory(Memory):
    _template = {'whatis': '%s是什么?', 'yes': '是', 'no': '不是', 'get': '我知道了',
     'unknown': '我不知道', 'think': '让我想一想', 'excuse':'能再说一遍吗？',
     'inconsistent': '与已知的不一致'}
    _dict = {'事物': 'Thing', '东西': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
    '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}
    _globals = globals().copy()

    def warning(self, s):
        return '\%s 应该是一个 %s.' % s


class ChineseConfig:
    def is_instance_of(self):
        return self.relation == '是'

    def is_kind_of(self):
        return self.relation == '是一种'

    def what_query(self):
        return self.query == '什么'

    def who_query(self):
        return self.query == '谁'

    def what_who_query(self):
        return self.query.content in {'谁', '什么'}

    def which_query(self):
        return self.query == '哪个'

    def which_kind_query(self):
        return self.query == '哪种'

config(SentenceAction, ChineseConfig)


word = pp.Word(pp.pyparsing_unicode.Chinese.alphanums)
word.addParseAction(ConceptAction)
ind = pp.QuotedString('"')
ind.addParseAction(IndividualAction)
noun = ind('content') | word('content')

SOME = pp.Literal('一些')
ONLY = pp.Literal('只')

Quantifier = SOME | ONLY
Quantifier.addParseAction(QuantifierAction)

dePhrase = noun + pp.Suppress('的') + noun

verb = pp.Word(pp.pyparsing_unicode.Chinese.alphas)
verb.addParseAction(RelationAction)

verb =  verb('content') | pp.Empty()

def sentence(subj, obj, relation):
    return (subj + pp.Suppress('的') + relation + pp.Suppress('是') + obj
        | obj + pp.Suppress('是') + subj + pp.Suppress('的') + relation
        | subj + pp.Suppress('与') + obj + relation
        | subj + relation + obj)

definition = noun('subj') + pp.Optional('不')('negative') + pp.Optional(SOME)('quantifier') + pp.oneOf(['是', '是一种'])('relation') + noun('obj')
definition.addParseAction(DefinitionAction)
statement = sentence(noun('subj'), noun('obj'), pp.Optional('不')('negative') + pp.Optional(ONLY)('quantifier') + verb('relation')  + pp.Optional(SOME)('quantifier'))
generalQuestion = statement.copy() + pp.Suppress('吗' + pp.Optional('？'))
generalQuestion.addParseAction(GeneralQuestionAction)
statement.addParseAction(StatementAction)

who = pp.Literal('谁')('content')
what = pp.Literal('什么')('content')
which = pp.Literal('哪个')('content') + noun('type')
which_kind = pp.Literal('哪种')('content') + noun('type')

def set_type(t, type_='人'):
    t.type = type_
    return t

who.addParseAction(set_type)
# who.addParseAction(VariableAction)
# what.addParseAction(VariableConceptAction)
# which.addParseAction(VariableAction)
# which_kind.addParseAction(VariableConceptAction)

query= who | what | which | which_kind
query.addParseAction(QueryAction)

specialQuestion = (sentence(query('query'), noun('obj'), pp.Optional('不')('negative') + verb('relation')) |
sentence(noun('subj'), query('query'), pp.Optional('不')('negative') + verb('relation'))) + pp.Suppress('？')
specialQuestion.addParseAction(SpecialQuestionAction)

question = specialQuestion | generalQuestion
sentence = question | definition | statement

def parse(s):
    return sentence.parseString(s, parseAll=True)[0]

# import jieba
# import logging
# jieba.setLogLevel(logging.INFO)
# 
# print(parse('狗 喜欢 什么 ？'))
