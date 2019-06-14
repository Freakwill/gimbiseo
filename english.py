#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Transform English to Logic Expressions

Example:
>>> res = english2logic('John isa Thing')
>>> print(res)
isa(John, Thing)
"""

import types

import pyparsing as pp
import pyparsing_ext as ppx


_dict = {'symmetric':'SymmetricProperty', 'thing':'Thing'}

class SentenceAction(ppx.BaseAction):
    def __init__(self, instring='', loc=0, tokens=[]):
        super(SentenceAction, self).__init__(instring, loc, tokens)
        self.relation = tokens.relation
        self.object = _dict.get(tokens.object, tokens.object)
        self.subject = _dict.get(tokens.subject, tokens.subject)

class GeneralQuestionAction(SentenceAction):

    def __str__(self):
        if self.has('relation') and self.relation:
            return '%s(%s, %s)?' % (self.relation, self.subject, self.object)
        else:
            return '%s(%s)?' % (self.object, self.subject)

    def exec(self, memory):
        if self.has('relation') and self.relation:
            # o in s.R.indirect()
            return memory[self.object] in getattr(memory[self.subject], self.relation).indirect()
        else:
            # s is an instance of o
            return isinstance(memory[self.subject], memory[self.object])

class SpecialQuestionAction(SentenceAction):

    def __str__(self):
        return '%s(%s, %s)?' % (self.relation, self.subject, self.object)

    def exec(self, memory):
        if self.object in {'Who', 'What'}:
            # {a.name | a in s.R.indirect()}
            return ', '.join(a.name for a in getattr(memory[self.subject], self.relation).indirect())
        elif self.subject in {'Who', 'What'}:
            # {a.name | a in s.R.inverse.indirect()}
            return ','.join(a.name for a in getattr(getattr(memory[self.subject], self.relation), 'inverse').indirect())

        
class StatementAction(SentenceAction):
    def __init__(self, instring='', loc=0, tokens=[]):
        super(StatementAction, self).__init__(instring, loc, tokens)
        if self.has('explain'):
            self.explain = tokens.explain

    def __str__(self):
        if self.has('explain') and self.explain:
            return '%s and %s(%s, %s)' % (self.explain, self.relation, self.subject, self.object)
        else:
            return '%s(%s, %s)' % (self.relation, self.subject, self.object)

    def exec(self, memory):
        if self.relation == 'is a':
            # s is an instance of o
            if self.subject in memory:
                memory[self.subject].is_instance_of.append(memory[self.object])
            else:
                # create s as an instance of o
                memory.update({self.subject: memory[self.object](self.subject)})
        elif self.relation in {'sort', 'kind'}:
            # s is a sort/kind of o
            if self.subject in memory:
                memory[self.subject].is_a.append(memory[self.object])
            else:
                # create s as a subclass of o
                memory.update({self.subject: types.new_class(self.subject, (memory[self.object],))})
        else:
            # create R as a relation between s and o
            memory.update({self.relation: types.new_class(self.relation, (type(memory[self.subject]) >> type(memory[self.object]),))})
            getattr(memory[self.subject], self.relation).extend([memory[self.object]])

    def to_gq(self):
        gq = GeneralQuestion()
        for p in ('relation', 'subject', 'object'):
            setattr(gq, p, getattr(self, p))


Noun = pp.Word(pp.alphanums)
Verb = pp.Word(pp.alphas)

Phrase = pp.Literal('a') + (Noun('relation') + 'of' + Noun('object') | Noun('object'))
GeneralQuestion = (pp.CaselessLiteral('Is') + Noun('subject') + Phrase \
| pp.CaselessLiteral('Dose') + Noun('subject') + Verb('relation') + Noun('object')) + '?'

SpecialQuestion = (pp.CaselessLiteral('What') | pp.CaselessLiteral('Who'))('object') + 'dose' + Noun('subject') + Verb('relation') \
    | (pp.CaselessLiteral('Who')('subject') + Verb('relation') + Noun('object') \
    | pp.CaselessLiteral('Which') + Noun('object') + 'dose' + Noun('subject') + Verb('relation')) + '?'
Question = SpecialQuestion.addParseAction(SpecialQuestionAction) | GeneralQuestion.addParseAction(GeneralQuestionAction)

Statement = pp.Forward()
Statement <<= Noun('subject') + (('is a' + Noun('relation') + 'of') | pp.Literal('is a')('relation') | Verb('relation')) + Noun('object') + pp.Optional(pp.Keyword('where') + Statement('explain'))
Statement.addParseAction(StatementAction)

Sentence = Question | Statement


def toLogic(s):
    return Sentence.parseString(s)[0]

