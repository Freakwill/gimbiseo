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
        raise NotImplementedError


class SentenceAction(BaseAction):
    names = ('subj', 'obj', 'relation', 'negative')

    def __str__(self):
        return self.toFormula()

    def toFormula(self):
        if self.is_instance_of():
            s = f'{self.obj}({self.subj})'
        else:
            s = f'{self.relation}({self.subj}, {self.obj})'

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

    def toDL(self):
        if isinstance(self.obj, IndividualAction):
            if 'negative' in self:
                return f'{self.subj}:~∃{self.relation}.{{{self.obj}}}'
            else:
                return f'{self.subj}:∃{self.relation}.{{{self.obj}}}'
        else:
            if 'negative' in self:
                if 'only' in self:
                    return f'{self.subj}:~∀{self.relation}.{self.obj}'
                else:
                    return f'{self.subj}:~∃{self.relation}.{self.obj}'
            else:    
                if 'only' in self:
                    return f'{self.subj}:∀{self.relation}.{self.obj}'
                else:
                    return f'{self.subj}:∃{self.relation}.{self.obj}'


class StatementAction(SentenceAction):

    def exec(self, memory, locals={}):
        
        subj = self.subj(memory, locals)
        obj = self.obj(memory, locals)
        relation = self.relation(memory, locals)
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
                if 'only' in self:
                    subj.is_a.append(relation.some(Not(obj)))
                else:
                    subj.is_a.append(relation.only(Not(obj)))
            else:    
                if 'only' in self:
                    subj.is_a.append(relation.only(obj))
                else:
                    subj.is_a.append(relation.some(obj))
        return True


class DefinitionAction(StatementAction):

    def exec(self, memory, locals={}):
        subj = self.subj(memory, locals, check=False)
        obj = self.obj(memory, locals)
        if self.is_instance_of():
            if subj:
                if 'negative' in self:
                    if obj in subj.INDIRECT_is_instance_of:
                        print(memory.inconsistent)
                    else:
                        subj.is_instance_of.append(Not(obj))
                else:
                    if Not(obj) in subj.INDIRECT_is_instance_of:
                        print(memory.inconsistent)
                    else:
                        subj.is_instance_of.append(obj)
            else:
                self.subj.new(memory, (obj.main,))
        elif self.is_kind_of():
            if self.subj.content in memory:
                if 'negative' in self:
                    if obj in subj.INDIRECT_is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(Not(obj))
                else:
                    if Not(obj) in subj.INDIRECT_is_a:
                        print(memory.inconsistent)
                    else:
                        subj.is_a.append(obj)
            else:
                self.subj.create(memory, (obj.main,))

        elif self.is_defined_as():
            self.subj.create(memory, (obj.main,), {'equivalent_to':[obj]})
        return True

    def toDL(self):
        if self.is_instance_of():
            if 'negative' in self:
                return f'{self.subj} : ~{self.obj.toDL()}'
            else:
                return f'{self.subj} : {self.obj.toDL()}'
        elif self.is_kind_of():
            if 'negative' in self:
                return f'{self.subj} <: ~{self.obj.toDL()}'
            else:
                return f'{self.subj} <: {self.obj.toDL()}'


class GeneralQuestionAction(SentenceAction):

    def toFormula(self):
        return super(GeneralQuestionAction, self).toFormula() + '?'

    def toDL(self):
        type = self.query.type
        return super(GeneralQuestionAction, self).toDL() + '?'
    
    def exec(self, memory, locals={}):
        subj = self.subj(memory, locals, check=False)
        obj = self.obj(memory, locals)
        if self.is_instance_of():
            if isinstance(self.obj, ConceptAction):
                ans = is_instance_of(subj, obj)
            else:
                ans = is_instance_of(obj, subj)
        elif self.is_kind_of():
            if isinstance(self.subj, ConceptAction):
                ans = is_a(subj, obj)
            else:
                ans = is_instance_of(subj, obj)
        else:
            if isinstance(self.obj, IndividualAction):
                ans = obj in getattr(subj, self.relation.content) or obj in getattr(subj, 'INDIRECT_'+self.relation)
            else:
                c = self.relation(memory).some(obj)
                if isinstance(self.subj, IndividualAction):
                    ans = is_instance_of(subj, c)
                else:
                    ans = is_a(subj, c)
        if 'negative' in self:
            return not ans
        else:
            return ans

class SpecialQuestionAction(GeneralQuestionAction):
    names = ('query',) + SentenceAction.names

    def toFormula(self):
        return super(GeneralQuestionAction, self).toFormula() + f' & {self.query}?'

    def toDL(self):
        return super(GeneralQuestionAction, self).toDL() + f' & {self.query.toDL()}?'

    @property
    def query(self):
        if isinstance(self.obj, VariableAction):
            return self.obj
        elif isinstance(self.subj, VariableAction):
            return self.subj
        else:
            raise Exception('Provide subj or obj')

    def sub(self, v):
        self.obj = self.obj.sub(v)
        self.subj = self.subj.sub(v)
        return self
 
    def exec(self, memory, locals={}):
        if isinstance(self.obj, VariableAction):
            known = self.subj(memory, locals)
            query = self.obj
            flag = 1
        elif isinstance(self.subj, VariableAction):
            known = self.obj(memory, locals)
            query = self.subj
            flag = 2
        else:
            raise Exception('Provide subj or obj')

        relation = self.relation(memory)
        if isinstance(query, VariableConceptAction):
            if flag == 1:
                if 'type' in query:
                    return ', '.join(X.name for X in getattr(known, 'INDIRECT_'+self.relation) if isinstance(X, ThingClass) and not is_a(query.type(memory, locals), X))
                else:
                    return ', '.join(X.name for X in getattr(known, 'INDIRECT_'+self.relation) if isinstance(X, ThingClass))
            else:
                clss = memory.clss
                if 'type' in query:
                    return ', '.join(X.name for X in clss if is_a(X, query.type(memory, locals)) and not is_a(query.type(memory, locals), X) and known in getattr(X, 'INDIRECT_'+self.relation))
                else:
                    return ', '.join(X.name for X in clss if isinstance(X, ThingClass) and known in getattr(X, 'INDIRECT_'+self.relation))
        else:
            if flag == 1:
                if 'type' in query:
                    return ', '.join(x.name for x in getattr(known, 'INDIRECT_'+self.relation) if isinstance(x, Thing) and is_instance_of(x, query.type(memory, locals)))
                else:
                    return ', '.join(x.name for x in getattr(known, 'INDIRECT_'+self.relation) if isinstance(x, Thing))
            else:
                inds = memory.inds
                if 'type' in query:
                    return ', '.join(x.name for x in inds if is_instance_of(x, query.type(memory, locals)) and known in getattr(a, 'INDIRECT_'+self.relation))
                else:
                    return ', '.join(x.name for x in inds if known in getattr(a, 'INDIRECT_'+self.relation))
        

class DefinitionQuestionAction(SpecialQuestionAction):
 
    def exec(self, memory, locals={}):
        if isinstance(self.obj, VariableAction):
            known = self.subj(memory, locals)
            query = self.obj
            flag = 1
        elif isinstance(self.subj, VariableAction):
            known = self.obj(memory, locals)
            query = self.subj
            flag = 2
        else:
            raise Exception('Provide subj or obj')

        if isinstance(query, VariableConceptAction):
            if isinstance(known, Thing):
                if 'type' in query:
                    Cs = set(known.INDIRECT_is_a) - {query.type(memory, locals)}
                    return ', '.join(X.name for X in proper(Cs) if hasattr(X, 'name') and not is_a(query.type(memory, locals), X))
                else:
                    Cs = set(known.INDIRECT_is_a) 
                    return ', '.join(X.name for X in proper(Cs) if hasattr(X, 'name'))
            else:
                if flag == 1:
                    if 'type' in query:
                        Cs = set(known.INDIRECT_is_a) - {query.type(memory, locals), known}
                        return ', '.join(X.name for X in proper(Cs) if hasattr(X, 'name') and not is_a(query.type(memory, locals), X))
                    else:
                        Cs = set(known.INDIRECT_is_a) - {known}   
                        return ', '.join(X.name for X in proper(Cs) if hasattr(X, 'name'))
                else:
                    if 'type' in query:
                        return ', '.join(X.name for X in memory.clss if is_a(X, known) and X != known and not is_a(query.type(memory, locals), X))
                    else:
                        return ', '.join(X.name for X in memory.clss if is_a(X, known) and X != known)
        else:
            if 'type' in query:
                return ', '.join(x.name for x in memory.inds if is_instance_of(x, query.type(memory, locals)) and is_instance_of(x, known))
            else:
                return ', '.join(x.name for x in memory.inds if is_instance_of(x, known))


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
        return self.toFormula()

    def eval(self, memory, locals={}, check=True):
        if self.content in locals:
            return locals[self.content]
        elif self.content in memory:
            return memory[self.content]
        else:
            if check:
                raise NameError(memory.whatis % self.content)
            else:
                return self.create(memory)

    def update(self, memory, x):
        return memory.update({self.content:x})

    def __radd__(self, s):
        return s + self.content

    @property
    def depth(self):
        return self._depth

    def containedin(self, memory):
        return self.content in memory

    def toDL(self):
        return self.content

    def sub(self, v):
        return self


class VariableAction(AtomAction):
    names = ('type',) + AtomAction.names
    value = ''

    def __str__(self):
        if 'type' in self:
            return f'x:{self.type}'
        else:
            return 'x'

    def toFormula(self):
        if 'type' in self:
            return f'{self.type}(x)'
        else:
            return 'Thing(x)'

    def toDL(self):
        if 'type' in self:
            return f'x:{self.type}'
        else:
            return 'x:Thing'

    def sub(self, v):
        if 'type' in self:
            if self.type in v.INDIRECT_is_instance_of:
                self.value = v
            else:
                raise TypeError(f'{v} is not a instance of {self.type}')
        else:
            self.value = v

    def eval(self, memory, locals={}):
        if self.content in locals:
            return locals[self.content]
        else:
            raise NameError(memory.uninterpreted % self.content)

class ConstantAction(AtomAction):
    pass

class IndividualAction(ConstantAction):
    def new(self, memory, klass=Thing):
        ind = klass(self.content)
        memory.update({self.content: ind})
        return ind

    def create(self, *args, **kwargs):
        return self.new(*args, **kwargs)

    def toConcept(self):
        return OneOf({self(memory)})

class VariableConceptAction(VariableAction):

    def __str__(self):
        if 'type' in self:
            return f'X:{self.type}'
        else:
            return 'X'

    def toFormula(self):
        if 'type' in self:
            return f'{self.type}(X)'
        else:
            return 'Thing(X)'

    def toDL(self):
        if 'type' in self:
            return f'X:{self.type}'
        else:
            return 'X:Thing'

    def sub(self, v):
        if 'type' in self:
            if self.type in v.is_a:
                self.value = v
            else:
                raise TypeError(f'{v} is not a instance of {self.type}')
        else:
            self.value = v

class ConceptAction(ConstantAction):

    def create(self, memory, bases=(Thing,), kwds=None):
        name = memory._dict.get(self.content, self.content)
        rel = types.new_class(name, bases, kwds)
        memory.update({name: rel})
        return rel

    @property
    def main():
        return self.content(memory)


class VpAction(ConceptAction):
    names = ('content', 'relation')
    def eval(self, memory, locals={}):
        rel = self.relation(memory, locals)
        A = self.content(memory, locals)
        if isinstance(self.content, IndividualAction):
            if 'negative' in self:
                if 'only' in self:
                    return rel.some(Not(OneOf({A})))
                else:
                    return rel.only(Not(OneOf({A})))
            else:
                if 'only' in self:
                    return rel.only(OneOf({A}))
                else:
                    return rel.value(A)
        else:
            if 'negative' in self:
                if 'only' in self:
                    return rel.some(Not(A))
                else:
                    return rel.only(Not(A))
            else:
                if 'only' in self:
                    return rel.only(A)
                else:
                    return rel.some(A)

    # def sub(self, v, *args, **kwargs):
    #     return self.eval(memory, locals={})

    def toFormula(self):
        if 'only' in self:
            return '%s*(?, %s)' % (self.relation, self.content)
        else:
            return '%s(?, %s)' % (self.relation, self.content)

    def toDL(self):
        if isinstance(self.content, IndividualAction):
            if 'negative' in self:
                if 'only' in self:
                    return f'∃{self.relation}.~{{{self.content}}}'
                else:
                    return f'∀{self.relation}.~{{{self.content}}}'
            else:
                if 'only' in self:
                    return f'∀{self.relation}.{{{self.content}}}'
                else:
                    return f'∃{self.relation}.{{{self.content}}}'
        else:
            if 'negative' in self:
                if 'only' in self:
                    return f'∃{self.relation}.~{self.content}'
                else:
                    return f'∀{self.relation}.~{self.content}'
            else:
                if 'only' in self:
                    return f'∀{self.relation}.{self.content}'
                else:
                    return f'∃{self.relation}.{self.content}'

class NpAction(ConceptAction):
    names = ('concepts', 'content')
    def eval(self, memory, locals={}):
        return And([concept(memory, locals) for concept in self.concepts] + [self.content(memory)])

    def toFormula(self):
        return f'({self.content} & {"& ".join(str(concept) for concept in self.concepts)})'

    def toDL(self):
        return f'({self.content} & {"& ".join(concept.toDL() for concept in self.concepts)})'

class CompoundConceptAction(ConceptAction):
    names = ('concepts',)
    def __init__(self):
        super(CompoundConceptAction, self).__init__()
        self.concepts = self.tokens

class AndAction(CompoundConceptAction):

    def eval(self, memory, locals={}):
        return And([concept(memory, locals) for concept in self.concepts])

    def toFormula(self):
        return "& ".join(str(concept) for concept in self.concepts)

    def toDL(self):
        return "& ".join(concept.toDL() for concept in self.concepts)


class OrAction(CompoundConceptAction):

    def eval(self, memory, locals={}):
        return Or([concept(memory, locals) for concept in self.concepts])

    def toFormula(self):
        return "| ".join(str(concept) for concept in self.concepts)

    def toDL(self):
        return "| ".join(concept.toDL() for concept in self.concepts)

class DeAction:
    names = ('owner', 'property')
    def eval(self, memory, locals={}):
        rel = self.property(memory, locals, bases=FunctionalProperty)
        A = self.owner(memory, locals)
        name = self.owner + '_'+ self.property
        x = memory.new_ind(name, klass=Thing)
        return x

    def toFormula(self):
        return f'{self.property}({self.owner})'


class RelationAction(ConstantAction):
    def eval(self, memory, locals={}, check=False):
        if self.content in memory:
            return memory[self.content]
        else:
            if check:
                raise NameError(memory.whatis % self.content)
            else:
                return self.create(memory)

    def create(self, memory, bases=(ObjectProperty,), kwds=None):
        rel = types.new_class(self.content, bases, kwds)
        memory.update({self.content: rel})
        return rel


class QuantifierAction(AtomAction):
    pass

def config(Action, Config):
    from inspect import getmembers
    from types import FunctionType
    for k, v in getmembers(Config, predicate=lambda x: isinstance(x, FunctionType)):
        setattr(Action, k, v)


# class QueryAction(VariableAction):
#     names = VariableAction.names + ('type',)
#     def toDL(self):
#         if self.content in {'谁', '哪个'}:
#             v = 'x'
#         else:
#             v = 'X'
#         if 'type' in self:
#             v += f':{self.type}'
#         return v
