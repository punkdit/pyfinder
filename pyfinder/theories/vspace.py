#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# 

scalar = Sort('scalar')
vector = Sort('vector')

zero = Constant(0, scalar)
one = Constant(1, scalar)
vzero = Constant(0, vector)

add = Function('add', [scalar, scalar], scalar)
neg = Function('neg', [scalar], scalar)
mul = Function('mul', [scalar, scalar], scalar)
inv = PartialFunction('inv', [scalar], scalar)

vadd = Function('vadd', [vector, vector], vector)
vneg = Function('vneg', [vector], vector)
vmul = Function('vmul', [scalar, vector], vector)

a = Variable('a', scalar)
b = Variable('b', scalar)
c = Variable('c', scalar)

x = Variable('x', vector)
y = Variable('y', vector)
z = Variable('z', vector)

sorts = [scalar, vector]
funcs = [neg, inv, add, mul, vneg, vadd, vmul]

theory = Theory([
    # Scalar field
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

    # Vector space
    vadd(x, vadd(y, z)) == vadd(vadd(x, y), z), # assoc
    vadd(x, y) == vadd(y, x), # comm
    vadd(vzero, x) == x, # ident
    vadd(x, vzero) == x, # ident
    vadd(x, vneg(x)) == vzero, # inverse
    vadd(vneg(x), x) == vzero, # inverse

    vmul(one, x) == x,
    vmul(a, vmul(b, x)) == vmul(mul(a, b), x), # assoc
    vmul(add(a, b), x) == vadd(vmul(a, x), vmul(b, x)), # dist
    vmul(a, vadd(x, y)) == vadd(vmul(a, x), vmul(a, y)), # dist
])





