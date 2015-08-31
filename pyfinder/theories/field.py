#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Field

scalar = Sort('scalar') # a field

zero = Constant(0, scalar)
one = Constant(1, scalar)

add = Function('add', [scalar, scalar], scalar)
neg = Function('neg', [scalar], scalar)
mul = Function('mul', [scalar, scalar], scalar)
inv = PartialFunction('inv', [scalar], scalar)

a = Variable('a', scalar)
b = Variable('b', scalar)
c = Variable('c', scalar)

theory = Theory([
    add(a, add(b, c)) == add(add(a, b), c), # assoc
    add(a, b) == add(b, a), # comm
    add(zero, a) == a, # ident
    add(a, zero) == a, # ident
    add(a, neg(a)) == zero, # inverse
    add(neg(a), a) == zero, # inverse

    mul(a, mul(b, c)) == mul(mul(a, b), c), # assoc
    mul(a, b) == mul(b, a), # comm
    mul(one, a) == a, # ident
    mul(a, one) == a, # ident
    (a!=zero).implies(inv(a).exists()),
    inv(a).exists().implies(a!=zero),
    (a!=zero).implies(mul(a, inv(a)) == one), # inverse
    (a!=zero).implies(mul(inv(a), a) == one), # inverse

    mul(add(a, b), c) == add(mul(a, c), mul(b, c)), # dist
    mul(a, add(b, c)) == add(mul(a, b), mul(a, c)), # dist
])


sorts = [scalar]
funcs = [neg, inv, add, mul]



