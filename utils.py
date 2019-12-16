#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from owlready2 import *

def is_instance_of(i, c, exclude=set()):
    # i: Thing, c: Concept/Class
    if i.INDIRECT_is_instance_of and c in i.INDIRECT_is_instance_of:
        return True
    if isinstance(c, And):
        return all(is_instance_of(i, cc, exclude) for cc in c.Classes)
    elif isinstance(c, Or):
        return any(is_instance_of(i, cc, exclude) for cc in c.Classes)
    elif isinstance(c, Not):
        return not is_instance_of(i, c, exclude)
    elif isinstance(c, OneOf):
        return all(i == x for x in c.instances)
    elif isinstance(c, Restriction):
        i_r = getattr(i, c.property.name)
        if i_r:
            if c.type == 24:
                return is_a(c.value, i_r)
            if c.type == 25:
                return is_a(i_r, c.value)
            elif c.type == 29:
                return c.value == i_r[0]
        else:
            return False
    else:
        if i.INDIRECT_is_instance_of:
            if c in i.INDIRECT_is_instance_of:
                return True
            else:
                # for y in i.INDIRECT_is_instance_of:
                #     if y not in exclude:
                #         if is_a(y, c, exclude):
                #             return True
                #         else:
                #             exclude.add(y)
                # else:
                return False
        else:
            return False


def is_a(x, c, exclude=set()):
    if x == c or c == Thing:
        return True
    elif hasattr(x, 'is_a') and c in x.is_a:
        return True
    elif hasattr(x, 'INDIRECT_is_a'):
        if c in x.INDIRECT_is_a:
            return True
        # else:
        #     for b in x.INDIRECT_is_a:
        #         if hasattr(c, 'INDIRECT_is_a') and b in c.INDIRECT_is_a:
        #             pass
        #         if b != x and b != Thing:
        #             if is_a(b, c):
        #                 return True

    if isinstance(c, And):
        return all(is_a(x, cc) for cc in c.Classes)
    elif isinstance(c, (IndividualValueList, list)):
        return x in c
    if isinstance(x, Or):
        return all(is_a(cc, c) for cc in x.Classes)
    elif isinstance(x, OneOf):
        return all(is_instance_of(xi, c) for xi in x.instances)
    elif isinstance(x, And):
        return any(is_a(xi, c) for xi in x.Classes)
    else:
        # for y in x.is_a:
        #     if hasattr(y, 'is_a') and y not in exclude:
        #         if is_a(y, c, exclude):
        #             return True
        #         else:
        #             exclude = exclude.add(y)
        # else:
        return False


def inf(As, C=None):
    # inf elements of As
    if C:
        As = [A for A in As if not is_a(C, A)]
        return inf(As)
    else:
        As = list(As)
        for _ in range(len(As)):
            A = As.pop(0)
            if not any(is_a(B, A) for B in As if hasattr(B,'is_a') and hasattr(B, 'INDIRECT_is_a')):
                As.append(A)
    return As


def sup(As, C=None):
    # sup elements of As not containing C
    if C:
        As = [A for A in As if not is_a(C, A)]
        return sup(As)
    else:
        As = list(As)
        for _ in range(len(As)):
            A = As.pop(0)
            if not any(is_a(A, B) for B in As):
                As.append(A)
    return As


def pretty(x):
    if hasattr(x, 'name'):
        return x.name
    elif isinstance(x, Restriction):
        if x.type in {29, 24}:
            return x.property.name + x.value.name
    else:
        return ','.join(pretty(cc) for cc in x.Classes)

