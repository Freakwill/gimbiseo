#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform Chinese to Logic Expressions
"""

import types

import pyparsing as pp
import pyparsing_ext as ppx


_dict = {'事物': 'Thing', '对称关系':'SymmetricProperty', '传递关系': 'TransitiveProperty', '自反关系':'SymmetricProperty',
 '函数关系':'FunctionalProperty', '反函数关系':'InverseFunctionalProperty', '反对称关系':'AsymmetricProperty', '非自反关系':'IrreflexiveProperty'}

class SentenceAction(ppx.BaseAction):
    names = ('first', 'second', 'relation', 'negative')

    def __str__(self):
        if self.relation == '是':
            s= '%s(%s)' % (self.second, self.first)
        else:
            s= '%s(%s, %s)' % (self.relation, self.first, self.second)
        if 'negative' in self:
            return self.negative + s
        else:
            return s


def check(exec):
    def f(obj, memory):
        if obj.relation in {'是', '是一种'}:
            if obj.second in memory:
                exec(obj, memory)
                return True
            else:  
                print(memory.template['whatis'] % obj.second)
        else:
            if obj.first in memory and obj.second in memory:
                exec(obj, memory)
                return True
            else:
                if obj.first not in memory:   
                    print(memory.template['whatis'] % obj.first)
                if obj.second not in memory:   
                    print(memory.template['whatis'] % obj.second)
    return f

class GeneralQuestionAction(SentenceAction):

    def __str__(self):
        return super(GeneralQuestionAction, self).__str__() + '?'

    @check
    def exec(self, memory):
        if self.relation == '是':
            return isinstance(memory[self.first], memory[self.second]) or memory[self.second] in memory[self.first].is_instance_of
        elif self.relation == '是一种':
            return subclasscheck(memory[self.first], memory[self.second]) or memory[self.second] in memory[self.first].is_a
        else:
            return memory[self.second] in getattr(memory[self.first], 'INDIRECT_'+self.relation)
            

class SpecialQuestionAction(SentenceAction):
    names = ('query',) + SentenceAction.names
    def __str__(self):
        if self.query in {'谁', '什么'}:
            s= '%s(%s, %s)?' % (self.relation, self.query, self.second)
        else:
            s= '%s(%s, %s)?' % (self.relation, self.first, self.second)

        if 'negative' in self:
            return self.negative + s
        else:
            return s
 
    @check
    def exec(self, memory):
        if self.relation == '是':
            if self.query == '谁':
                known=memory[self.first] if 'first' in self else memory[self.second]
                return ', '.join(a.name for k, a in memory.items() if known in a.is_instance_of and a.is_instance_of(memory['人']))
            elif self.query == '什么':
                known=memory[self.first] if 'first' in self else memory[self.second]
                if isinstance(known, Thing):
                    return ', '.join(a.name for k, a in memory.items() if a in known.is_instance_of)
                else:
                    return ', '.join(a.name for k, a in memory.items() if known in a.is_instance_of)
        elif self.relation == '是一种':
            if self.query == '什么':
                if 'first' in self:
                    known = memory[self.first]
                    return ', '.join(a.name for k, a in memory.items() if a in known.is_a)
                else:
                    known = memory[self.second]
                    return ', '.join(a.name for k, a in memory.items() if known in a.is_a)
        else:
            if self.query == '谁':
                if 'first' in self:
                    known = memory[self.first]
                    return ', '.join(a.name for a in getattr(known, 'INDIRECT_'+self.relation) and a.is_instance_of(memory['人']))
                else:
                    known = memory[self.second]
                    return ', '.join(a.name for a in getattr(getattr(known, 'INDIRECT_'+self.relation), 'inverse')() and a.is_instance_of(memory['人']))
            elif self.query == '什么':
                if 'first' in self:
                    known = memory[self.first]
                    return ', '.join(a.name for a in getattr(known, 'INDIRECT_'+self.relation))
                else:
                    known = memory[self.second]
                    return ', '.join(a.name for a in getattr(getattr(known, 'INDIRECT_'+self.relation), 'inverse')())

        
class StatementAction(SentenceAction):
    
    # def __init__(self, instring='', loc=0, tokens=[]):
    #     super(StatementAction, self).__init__(instring, loc, tokens)
    #     # if 'explain' in self:
    #     #     self.explain = tokens.explain
    
    @check
    def exec(self, memory):
        if self.relation == '是':
            if self.first in memory:
                memory[self.first].is_instance_of.append(memory[self.second])
            else:
                memory.update({self.first: memory[self.second](self.first)})
        elif self.relation == '是一种':
            if self.first in memory:
                memory[self.first].is_a.append(memory[self.second])
            else:
                memory.update({self.first: types.new_class(self.first, (memory[self.second],))})
        else:
            memory.update({self.relation: types.new_class(self.relation, (type(memory[self.first]) >> type(memory[self.second]),))})
            getattr(memory[self.first], self.relation).extend([memory[self.second]])

Noun = pp.Word(pp.pyparsing_unicode.Chinese.alphanums)
Verb = pp.Word(pp.pyparsing_unicode.Chinese.alphas)

'''
金秘书爱李英俊。
谁爱李英俊？
我爱学习。
我爱什么？
我爱学习吗？
我的爱人是李英俊
'''

def sentence(first, second, relation):
    return (first + pp.Suppress('的') + relation + pp.Suppress('是') + second
        | second + pp.Suppress('是') + first + pp.Suppress('的') + relation
        |first + relation + second
        )

statement = sentence(Noun('first'), Noun('second'), pp.Optional('不')('negative') + Verb('relation'))
generalQuestion = statement + pp.Suppress('吗' + pp.Optional('？'))

who = pp.Literal('谁')
what = pp.Literal('什么')
which = pp.Literal('哪个') | pp.Literal('哪种')

specialQuestion = (sentence(who('query') |what('query') | which('query')+Noun('first'), Noun('second'), pp.Optional('不')('negative') + Verb('relation')) |
sentence(Noun('first'), what('query') | which('query')+Noun('second'), pp.Optional('不')('negative') + Verb('relation'))) + pp.Suppress('？')

question = specialQuestion.addParseAction(SpecialQuestionAction) | generalQuestion.addParseAction(GeneralQuestionAction)
sentence = question | statement.addParseAction(StatementAction)

def toLogic(s):
    return sentence.parseString(s, parseAll=True)[0]

# import jieba
# import logging
# jieba.setLogLevel(logging.INFO)
print(toLogic('谁 不 喜欢 小明？'))
