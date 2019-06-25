#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import types
from utils import *
from owlready2 import *

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



class SentenceAction(BaseAction):
    names = ('subj', 'obj', 'relation', 'negative')

    def __str__(self):
        return self.toFormula()

    def toFormula(self):
        if self.is_instance_of():
            s= '%s(%s)' % (self.obj, self.subj)
        else:
            s= '%s(%s, %s)' % (self.relation, self.subj, self.obj)
        if 'negative' in self:
            return self.negative + s
        else:
            return s

    def check(self, memory):
        try:
            subj = self.subj(memory)
        except Exception as e:
            print(e)
            return
        try:
            obj = self.obj(memory)
        except Exception as e:
            print(e)
            return
        return subj, obj

    def __call__(self, memory):
        return self.exec(memory)

class StatementAction(SentenceAction):

    def exec(self, memory):
        
        subj = self.subj(memory)
        obj = self.obj(memory)
        if self.is_instance_of():
            if subj:
                if 'negative' in self:
                    if obj in subj.is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(Not(obj))
                else:
                    if Not(obj) in subj.is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(obj)
            else:
                self.subj.create(memory, obj)
        elif self.is_kind_of():
            if subj:
                if 'negative' in self:
                    if obj in subj.is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(Not(obj))
                else:
                    if Not(obj) in subj.is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(obj)
            else:
                self.subj.create(memory, obj)
        else:
            if self.relation.content not in memory:
                relation = self.relation.create(memory, ObjectProperty)
            else:
                relation = self.relation(memory)
            if isinstance(self.obj, IndividualAction):
                if 'negative' in self:
                    subj.is_a.append(Not(relation.value(obj)))
                else:
                    if isinstance(self.subj, IndividualAction):
                        getattr(subj, self.relation.content).append(obj)
                    else:
                        subj.is_a.append(relation.value(obj))
            else:
                if 'negative' in self:
                    if 'quantifier' in self:
                        subj.is_a.append(relation.some(Not(obj)))
                    else:
                        subj.is_a.append(relation.only(Not(obj)))
                else:    
                    if 'quantifier' in self:
                        subj.is_a.append(relation.only(obj))
                    else:
                        subj.is_a.append(relation.some(obj))
        return True


class DefinitionAction(StatementAction):

    def exec(self, memory):
        subj = self.subj(memory, check=False)
        obj = self.obj(memory)
        if self.is_instance_of():
            if subj:
                if 'negative' in self:
                    if obj in subj.is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(Not(obj))
                else:
                    if Not(obj) in subj.is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(obj)
            else:
                self.subj.create(memory, obj)
        elif self.is_kind_of():
            if self.subj.content in memory:
                if 'negative' in self:
                    subj.is_a.append(Not(obj))
                else:
                    subj.is_a.append(obj)
            else:
                self.subj.create(memory, obj)
        return True

class GeneralQuestionAction(SentenceAction):

    def toFormula(self):
        return super(GeneralQuestionAction, self).toFormula() + '?'

    def exec(self, memory):
        obj = self.obj(memory)
        subj = self.subj(memory)
        if self.is_instance_of():
            return isinstance(subj, obj) or obj in subj.is_a
        elif self.is_kind_of():
            return issubclass(subj, obj) or obj in subj.is_a
        else:
            if isinstance(self.obj, IndividualAction):
                return obj in getattr(subj, self.relation.content) or obj in getattr(subj, 'INDIRECT_'+self.relation)
            else:
                c = self.relation(memory).some(obj)
                if isinstance(self.subj, IndividualAction):
                    return is_instance_of(subj, c)
                else:
                    return is_a(subj, c)

class SpecialQuestionAction(SentenceAction):
    names = ('query',) + SentenceAction.names

    def toFormula(self):
        if 'subj' in self:
            s= '%s(%s, %s)?' % (self.relation, self.subj, self.query)
        elif 'obj' in self:
            s= '%s(%s, %s)?' % (self.relation, self.query, self.obj)
        else:
            s= '%s(%s, %s)?' % (self.relation, self.subj, self.obj)

        if 'negative' in self:
            return self.negative + s
        else:
            return s
 
    def exec(self, memory):
        if 'subj' in self:
            subj = self.subj(memory)
            known = subj
        elif 'obj' in self:
            obj = self.obj(memory)
            known = obj
        else:
            raise Exception('Provide subj or obj')
        if self.is_instance_of():
            if self.who_query():
                # a for a in known.instances if isinstance(a, memory['Person'])
                return ', '.join(k for k, a in memory.items() if is_a(a, known) and isinstance(a, memory['Person']))
            elif self.what_query():
                if isinstance(known, IndividualAction):
                    return ', '.join(A.name for A in proper(known.is_instance_of) if hasattr(A, 'name'))
                else:
                    # known.instances
                    return ', '.join(k for k, a in memory.items() if is_a(a, known))
            elif self.which_query():
                if isinstance(known, IndividualAction):
                    return ', '.join(A.name for A in proper(known.is_instance_of) if hasattr(A, 'name'))
                else:
                    return ', '.join(k for k, a in memory.items() if is_a(a, known) and  isinstance(a, memory['subj']))
                    
        elif self.is_kind_of():
            if self.what_query():
                if 'subj' in self:
                    return ', '.join(A.name for A in proper(known.is_a) if hasattr(A, 'name'))
                else:
                    return ', '.join(k for k, a in memory.items() if is_a(a, known))
        else:
            if self.who_query():
                if 'subj' in self:
                    return ', '.join(a.name for a in getattr(known, 'INDIRECT_'+self.relation) and memory['Person'] in a.is_instance_of)
                else:
                    return ', '.join(a.name for k, a in memory if memory['Person'] in a.is_instance_of and known in getattr(a, 'INDIRECT_'+self.relation))
            elif self.what_query():
                if 'subj' in self:
                    return ', '.join(a.name for a in getattr(known, 'INDIRECT_'+self.relation))
                else:
                    return ', '.join(a.name for k, a in memory if isinstance(a, Thing) and known in getattr(a, 'INDIRECT_'+self.relation))
            # elif self.which_query():
            #     if isinstance(known, ConceptAction):
            #         return ', '.join(k for k, a in memory.items() if is_a(a, known) and  isinstance(a, memory['subj']))
            #     else:
            #         return ', '.join(k for k, a in memory.items() if is_a(known, a))


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


    def __eq__(self, other):
        if isinstance(other, str):
            return self.content == other
        else:
            return self.content == other.content

    def toFormula(self):
        return self.content

    def __str__(self):
        return self.content

    def eval(self, memory, check=True):
        if self.content in memory:
            return memory[self.content]
        else:
            if check:
                raise NameError(memory.whatis % self.content)
            else:
                return self.create(memory, Thing)

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
    names = ('type',) + AtomAction.names
    value = ''

    def __str__(self):
        if 'type' in self:
            return f'x:{self.type}'
        else:
            return 'x'

class ConstantAction(AtomAction):
    pass

class IndividualAction(ConstantAction):
    def create(self, memory, klass):
        ind = klass(self.content)
        memory.update({self.content: ind})
        return ind

    def toConcept(self):
        return OneOf({self(memory)})

class VariableConceptAction(VariableAction):

    def __str__(self):
        if 'type' in self:
            return f'X:{self.type}'
        else:
            return 'X'

class ConceptAction(ConstantAction):

    def create(self, memory, *bases):
        rel = types.new_class(self.content, bases=bases)
        memory.update({self.content: rel})
        return rel

class RelationAction(ConstantAction):
    def eval(self, memory, check=False):
        if self.content in memory:
            return memory[self.content]
        else:
            if check:
                raise NameError(memory.whatis % self.content)
            else:
                return self.create(memory, ObjectProperty)

    def create(self, memory, *bases):
        rel = types.new_class(self.content, bases=bases)
        memory.update({self.content: rel})
        return rel


class QuantifierAction(AtomAction):
    pass

def config(Action, Config):
    from inspect import getmembers
    from types import FunctionType
    for k, v in getmembers(Config, predicate=lambda x: isinstance(x, FunctionType)):
        setattr(Action, k, v)


class QueryAction(VariableAction):
    pass
