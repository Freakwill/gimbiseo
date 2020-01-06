#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform Chinese to Logic Expressions
"""

import warnings
warnings.filterwarnings("ignore")

import types

import pyparsing as pp

from .actions import *
from .chinese_cut import *
from .memory import *

class ChineseMemory(Memory):
    _template = {'whatis': '%s是什么?', 'yes': '是', 'no': '不是', 'iget': '我知道了', 'none':'不知道',
     'unknown': '我不知道', 'think': '让我想一想', 'excuse':'能再说一遍吗？',
     'inconsistent': '与已知的不一致', 'uninterpreted':'疑问词"%s"没有被解释',
     'no_repeat': '不要重复'
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

    def only(self):
        return 'quantifier' in self and self.quantifier == '只'

    def exactly(self):
        return 'quantifier' in self and self.quantifier.content in {'只', '正好', '恰好'} and 'number' in self

    def atleast(self):
        return 'quantifier' in self and self.quantifier == '至少' and 'number' in self

    def atmost(self):
        return 'quantifier' in self and self.quantifier == '至多' and 'number' in self


config(SentenceAction, ChineseConfig)
config(VpAction, ChineseConfig)

unpack = lambda l,s,t:t[0]

word = pp.Word(pp.pyparsing_unicode.Chinese.alphas)('content')
word.addParseAction(ConceptAction)

ind = pp.QuotedString('"')('content')
ind.addParseAction(IndividualAction)
noun = ind | word

SOME = pp.Literal('某些')
ONLY = pp.Literal('只')
ATLEAST = pp.Literal('至少')
ATMOST = pp.Literal('至多')

Quantifier = pp.Optional('q:').suppress() + (SOME | ONLY | ATLEAST | ATMOST)('content')
Quantifier.addParseAction(QuantifierAction)

verb = pp.Suppress('v:') + pp.Word(pp.pyparsing_unicode.Chinese.alphas)('content')
verb.addParseAction(RelationAction)

concept = pp.Forward()
qverb = pp.Optional(Quantifier('quantifier')) + verb('relation') + pp.Optional(SOME)('quantifier')
vp = pp.Optional('不')('negative') + qverb + noun
nv = pp.Optional('不')('negative') + noun + verb
vp.addParseAction(VpAction)
nv.addParseAction(NvAction)
adj = pp.Suppress('a:') + word | vp + pp.Suppress('的') | nv + pp.Suppress('的')
np = pp.OneOrMore(adj)('concepts') + word
np.addParseAction(NpAction)

# de = noun('owner') + pp.Keyword('的') + word('property')
# de.addParseAction(DeAction)
is_ =  pp.Optional('也')+ pp.oneOf(['是', '是一种', '定义为'])('relation')

ands = pp.delimitedList(noun, delim="c:和")('concepts')
ands.addParseAction(AndAction)

concept <<= np | adj | noun

subj = (pp.Suppress('a:') + word | noun)('subj')
subj.addParseAction(unpack)
definition = subj + pp.Optional('不')('negative') + is_ + concept('obj')
statement = subj + pp.Optional('不')('negative') +  (qverb + pp.pyparsing_common.integer('number') + '个' | qverb) + concept('obj')
#statementq = noun('subj')+ pp.Optional('不')('negative') + Quantifier('quantifier') + verb('relation') + pp.pyparsing_common.integer('number') + concept('obj')

generalQuestion = (definition.copy()|statement.copy()) + pp.Suppress('ma' + pp.Optional('？'))

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

specialQuestion = (query('subj').addParseAction(unpack) + pp.Optional('不')('negative') + verb('relation') + concept('obj') |
subj + pp.Optional('不')('negative') + verb('relation') + query('obj').addParseAction(unpack)) + pp.Suppress('？')
specialQuestion.addParseAction(SpecialQuestionAction)

definitionQuestion = (query('subj').addParseAction(unpack) + pp.Optional('不')('negative') + is_ + concept('obj') |
concept('subj') + pp.Optional('不')('negative') + is_ + query('obj').addParseAction(unpack)) + pp.Suppress('？')
definitionQuestion.addParseAction(DefinitionQuestionAction)

# sentences = pp.delimitedList(definition | statement, delim="；")('sentences')
# sentences.addParseAction(SentencesAction)

question = specialQuestion | definitionQuestion |generalQuestion
sentence = (question | definition | statement) + pp.Optional(pp.pythonStyleComment)

def parse(s, cut=True):
    if cut:
        s = s.partition('#')[0]
        s = cut_flag(s)
    return sentence.parseString(s, parseAll=True)[0]

