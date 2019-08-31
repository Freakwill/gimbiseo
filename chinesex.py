#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform Chinese to Logic Expressions
"""

import warnings
warnings.filterwarnings("ignore")

import types

import pyparsing as pp
import pyparsing_ext as ppx

from actions import *
from chinese_cut import *

class ChineseMemory(Memory):
    _template = {'whatis': '%s是什么?', 'yes': '是', 'no': '不是', 'get': '我知道了',
     'unknown': '我不知道', 'think': '让我想一想', 'excuse':'能再说一遍吗？',
     'inconsistent': '与已知的不一致', 'uninterpreted':'疑问词"%s"没有被解释'
     }
    _dict = {'事物': 'Thing', '性质': 'Thing', '人':'Person', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
 '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}
    _globals = globals().copy()

    def warning(self, s):
        return '\%s 应该是一个 %s.' % s


class ChineseConfig:
    def is_instance_of(self):
        return self.relation == '是'

    def is_kind_of(self):
        return self.relation == '是一种'

    def is_defined_as(self):
        return self.relation == '定义为'

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

word = pp.Word(pp.pyparsing_unicode.Chinese.alphas)('content')
word.addParseAction(ConceptAction)

ind = pp.QuotedString('"')('content')
ind.addParseAction(IndividualAction)
noun = ind | word

SOME = pp.Literal('某些')
ONLY = pp.Literal('只')
ATLEAST = pp.Literal('至少')
ATMOST = pp.Literal('至多')

Quantifier = SOME | ONLY
Quantifier.addParseAction(QuantifierAction)

verb = pp.Suppress('v:') + pp.Word(pp.pyparsing_unicode.Chinese.alphas)('content')
verb.addParseAction(RelationAction)

concept = pp.Forward()
vp = pp.Optional('不')('negative') + pp.Optional(Quantifier)('quantifier') + verb('relation') + noun
vp.addParseAction(VpAction)

adj = vp + pp.Suppress('的') | pp.Suppress('a:') + word

np = pp.OneOrMore(adj)('concepts') + word
np.addParseAction(NpAction)

# de = noun('owner') + pp.Keyword('的') + word('property')
# de.addParseAction(DeAction)
is_ =  pp.Optional('也')+ pp.oneOf(['是', '是一种', '定义为'])('relation')

concept <<= noun | np | adj

definition = noun('subj') + pp.Optional('不')('negative') + is_ + concept('obj')
statement = noun('subj')+ pp.Optional('不')('negative') + pp.Optional(Quantifier)('quantifier') + verb('relation') + pp.Optional(SOME)('quantifier') + concept('obj')
#statementq = noun('subj')+ pp.Optional('不')('negative') + Quantifier('quantifier') + verb('relation') + pp.pyparsing_common.integer('number') + concept('obj')

generalQuestion = (definition.copy()|statement.copy()) + pp.Suppress('吗' + pp.Optional('？'))

definition.addParseAction(DefinitionAction)
statement.addParseAction(StatementAction)
generalQuestion.addParseAction(GeneralQuestionAction)

who = pp.Literal('谁')('content')
what = pp.Literal('什么')('content')
which = pp.Literal('哪个')('content') + noun('type')
which_kind = (pp.Literal('哪种')('content') | pp.Literal('什么样的')('content') | pp.Literal('什么')('content')) + noun('type')

def set_type(l,s,t, type_='人'):
    t.type = type_
    return t

who.addParseAction(set_type)
# who.addParseAction(VariableAction)
# what.addParseAction(VariableConceptAction)
# which.addParseAction(VariableAction)
# which_kind.addParseAction(VariableConceptAction)

query1 = who | which
query2 = which_kind | what
query1.addParseAction(VariableAction)
query2.addParseAction(VariableConceptAction)
query = query1 | query2

specialQuestion = (query('subj').addParseAction(lambda l,s,t:t[0]) + pp.Optional('不')('negative') + verb('relation') + noun('obj') |
noun('subj') + pp.Optional('不')('negative') + verb('relation') + query('obj').addParseAction(lambda l,s,t:t[0])) + pp.Suppress('？')
specialQuestion.addParseAction(SpecialQuestionAction)

definitionQuestion = (query('subj').addParseAction(lambda l,s,t:t[0]) + pp.Optional('不')('negative') + is_ + concept('obj')|
concept('subj') + pp.Optional('不')('negative') + is_ + query('obj').addParseAction(lambda l,s,t:t[0])) + pp.Suppress('？')
definitionQuestion.addParseAction(DefinitionQuestionAction)

question = definitionQuestion | specialQuestion | generalQuestion
sentence = question | definition | statement

def parse(s, cut=False):
    if cut:
        s = cut_flag(s)
    return sentence.parseString(s, parseAll=True)[0]

# x = parse('"月球" 是 v:围绕 "地球" 的 卫星 吗？')
# print(x)
