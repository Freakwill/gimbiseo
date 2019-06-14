#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform Chinese to Logic Expressions
"""

import types

import pyparsing as pp
import pyparsing_ext as ppx

from gimbiseo.actions import *

_dict = {'事物': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
 '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}


class ChineseConfig:
    def is_linking(self):
        return self.relation == '是'

    def is_kindOf(self):
        return self.relation == '是一种'

    def what_query(self):
        return self.query == '什么'

    def who_query(self):
        return self.query == '谁'

    def what_who_query(self):
        return self.query in {'谁', '什么'}

    def which_query(self):
        return self.query == '哪个'

    def which_kind_query(self):
        return self.query == '哪种'

config(SentenceAction, ChineseConfig)

''' Examples
金秘书爱李英俊。
谁爱李英俊？
我爱学习。
我爱什么？
我爱学习吗？
我的爱人是李英俊
'''

CNoun = pp.Word(pp.pyparsing_unicode.Chinese.alphanums)
CNoun.addParseAction(ConceptAction)
INoun = pp.QuotedString('"')
INoun.addParseAction(IndividualAction)
Noun = INoun('content') | CNoun('content')

DePhrase = Noun + pp.Suppress('的') + Noun

Verb = pp.Word(pp.pyparsing_unicode.Chinese.alphas)
Verb.addParseAction(RelationAction)

Verb=  Verb('content') | Verb('content')

def sentence(first, second, relation):
    return (first + pp.Suppress('的') + relation + pp.Suppress('是') + second
        | second + pp.Suppress('是') + first + pp.Suppress('的') + relation
        | first + relation + second)

statement = sentence(Noun('first'), Noun('second'), pp.Optional('不')('negative') + Verb('relation'))
generalQuestion = statement.copy() + pp.Suppress('吗' + pp.Optional('？'))
generalQuestion.addParseAction(GeneralQuestionAction)
statement.addParseAction(StatementAction)

who = pp.Literal('谁')
what = pp.Literal('什么')
which = pp.Literal('哪个') + Noun('type')
which_kind = pp.Literal('哪种') + Noun('type')

def set_type(t, type_='人'):
    t.type = type_
    return t

who.addParseAction(set_type).addParseAction(VariableAction)
what.addParseAction(VariableAction)
which.addParseAction(VariableAction)
which_kind.addParseAction(VariableConceptAction)

specialQuestion = (sentence(who('query') |what('query') | which('query') | which_kind('query'), Noun('second'), pp.Optional('不')('negative') + Verb('relation')) |
sentence(Noun('first'), what('query') | which('query') | which_kind('query'), pp.Optional('不')('negative') + Verb('relation'))) + pp.Suppress('？')
specialQuestion.addParseAction(SpecialQuestionAction)

question = specialQuestion | generalQuestion
sentence = question | statement

def toLogic(s):
    return sentence.parseString(s, parseAll=True)[0]

# import jieba
# import logging
# jieba.setLogLevel(logging.INFO)

