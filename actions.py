#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import types

class BaseAction:
    '''Base class for parsing action classes

    Register the names of tokens in names list.
    '''
    names = ()
    def __init__(self, instring='', loc=0, tokens=[]):
        self.tokens = tokens
        self.instring = instring
        self.loc = loc
        for name in self.names:
            if name in tokens:
                setattr(self, name, getattr(tokens, name))

    def __contains__(self, name):
        return name in self.tokens

    def __len__(self):
        return len(self.tokens)

    def __eq__(self, other):
        if isinstance(other, BaseAction):
            return self.tokens == other.tokens
        else:
            return self.tokens == other

    def __repr__(self):
        return ' '.join(map(str, self.tokens))

    def __call__(self, *args, **kwargs):
        # if eval defined in action
        return self.eval(*args, **kwargs)

    def eval(self, *args, **kwargs):
        # evaluate it
        pass


def check(exec):
    def f(obj, memory):
        if obj.is_linking():
            if obj.second.content in memory:
                if isinstance(obj.second, ConceptAction):
                    return exec(obj, memory)
                else:
                    print('%s should be a concept' % obj.second)
            else:  
                print(memory.whatis % obj.second)
        elif obj.is_kindOf():
            if obj.first.content in memory and not isinstance(obj.first, (ConceptAction, RelationAction)):
                print('%s should be a concept or a relation' % obj.first)
            elif obj.second.content in memory:
                if isinstance(obj.second, ConceptAction):
                    return exec(obj, memory)
                else:
                    print('%s should be a concept' % obj.second)
            else:  
                print(memory.whatis % obj.second)
        else:
            if obj.first.content in memory and obj.second.content in memory:
                if isinstance(obj.first, IndividualAction):
                    return exec(obj, memory)
                else:
                    print('%s should be an individual' % obj.first)
            else:
                if obj.first.content not in memory:   
                    print(memory.whatis % obj.first)
                if obj.second.content not in memory:   
                    print(memory.whatis % obj.second)
    return f

class SentenceAction(BaseAction):
    names = ('first', 'second', 'relation', 'negative')

    def __str__(self):
        return self.toFormula()

    def toFormula(self):
        if self.is_linking():
            s= '%s(%s)' % (self.second, self.first)
        else:
            s= '%s(%s, %s)' % (self.relation, self.first, self.second)
        if 'negative' in self:
            return self.negative + s
        else:
            return s

    def exec(self, memory):
        pass

    def __call__(self, memory):
        return self.exec(memory)

class StatementAction(SentenceAction):

    @check
    def exec(self, memory):
        first = self.first(memory)
        second = self.second(memory)
        if self.is_linking():
            if first:
                if 'negative' in self:
                    first.is_a.append(Not(second))
                else:
                    first.is_a.append(second)
            else:
                self.first.create(memory, second)
        elif self.is_kindOf():
            if self.first.content in memory:
                if 'negative' in self:
                    first.is_a.append(Not(second))
                else:
                    first.is_a.append(second)
            else:
                self.first.create(memory, second)
        else:
            if self.relation.content not in memory:
                self.relation.create(memory, type(first) >> type(second))
            if isinstance(self.second, IndividualAction):
                if 'negative' in self:
                    first.is_a.apppend(Not(second.value(self.second)))
                else:
                    getattr(first, self.relation.content).append(second)
            else:
                if 'negative' in self:
                    first.is_a.apppend(Not(second.some(self.second)))
                else:
                    first.is_a.apppend(second.some(self.second))
        return True


class GeneralQuestionAction(SentenceAction):

    def toFormula(self):
        return super(GeneralQuestionAction, self).toFormula() + '?'

    @check
    def exec(self, memory):
        first = self.first(memory)
        second = self.second(memory)
        if self.is_linking():
            return isinstance(first, second) or second in first.is_a
        elif self.is_kindOf():
            return issubclass(first, second) or second in first.is_a
        else:
            if isinstance(self.second, IndividualAction):
                return second in getattr(first, 'INDIRECT_'+self.relation)
            else:
                return self.relation(memory).some(second) in first.is_a

class SpecialQuestionAction(SentenceAction):
    names = ('query',) + SentenceAction.names
    def toFormula(self):
        if self.what_who_query():
            s= '%s(%s, %s)?' % (self.relation, self.query, self.second)
        else:
            s= '%s(%s, %s)?' % (self.relation, self.first, self.second)

        if 'negative' in self:
            return self.negative + s
        else:
            return s
 
    @check
    def exec(self, memory):
        if 'first' in self:
            first = self.first(memory)
            known = first
        if 'second' in self:
            second = self.second(memory)
            known = second
        if self.is_linking:
            if self.who_query():
                known = first if 'first' in self else second
                return ', '.join(k for k, a in memory.items() if known in a.is_a and isinstance(a, memory['Person']))
            elif self.what_query():
                if isinstance(known, ConceptAction):
                    return ', '.join(k for k, a in memory.items() if known in a.is_a)
                else:
                    return ', '.join(k for k, a in memory.items() if a in known.is_a)
            # elif self.which_query():
            #     if isinstance(known, ConceptAction):
            #         return ', '.join(k for k, a in memory.items() if known in a.is_a and  isinstance(a, memory['first']))
            #     else:
            #         return ', '.join(k for k, a in memory.items() if a in known.is_a)
        elif self.is_kindOf:
            if self.what_query():
                if isinstance(known, ConceptAction):
                    return ', '.join(k for k, a in memory.items() if a in known.is_a)
                else:
                    return ', '.join(k for k, a in memory.items() if known in a.is_a)
        else:
            if self.who_query():
                if 'first' in self:
                    return ', '.join(a.name for a in getattr(known, 'INDIRECT_'+self.relation) and memory['人'] in a.is_instance_of)
                else:
                    return ', '.join(a.name for a in getattr(getattr(known, 'INDIRECT_'+self.relation), 'inverse')() and memory['Person'] in a.is_instance_of)
            elif self.what_query():
                if 'first' in self:
                    return ', '.join(a.name for a in getattr(known, 'INDIRECT_'+self.relation))
                else:
                    return ', '.join(a.name for a in getattr(getattr(known, 'INDIRECT_'+self.relation), 'inverse')())

class CompoundSentenceAction(BaseAction):
    names = ('conjunction', 'sentences')

    def toFormula(self):
        return self.conjunction.join(x.toFormula for x in self.sentences)

    @property
    def depth(self):
        return sum(s.depth for s in self.sentences) + 1
    

class AtomAction(BaseAction):
    names = ('content',)
    _depth = 1

    def toFormula(self):
        return self.content

    def eval(self, memory):
        if self.content in memory:
            return memory[self.content]

    def update(self, memory, x):
        return memory.update({self.content:x})

    def __radd__(self, s):
        return s + self.content

    @property
    def depth(self):
        return self._depth

    def containedin(self, memory):
        return self.content in memory


class VariableAction(AtomAction):
    names = ('type',)
    value = ''

    def eval(self, memory):
        if 'type' in self:
            return f'x:{self.type}'
        else:
            return 'x'

class ConstantAction(AtomAction):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.content == other
        else:
            return self.content == other.content

class IndividualAction(ConstantAction):
    def create(self, memory, klass):
        memory.update({self.content: klass(self.content)})

class VariableConceptAction(AtomAction):
    names = ('type',)
    value = ''

    def eval(self, memory):
        if 'type' in self:
            return f'X:{self.type}'
        else:
            return 'X'

class ConceptAction(ConstantAction):
    def create(self, memory, *bases):
        memory.update({self.content: types.new_class(self.content, bases=bases)})

class RelationAction(ConstantAction):
    def create(self, memory, *bases):
        memory.update({self.content: types.new_class(self.content, bases=bases)})


def config(Action, Config):
    from inspect import getmembers
    from types import FunctionType
    for k, v in getmembers(Config, predicate=lambda x: isinstance(x, FunctionType)):
        setattr(Action, k, v)

