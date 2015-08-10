#!/usr/bin/env python

from expr import *

#______________________________________________________________________________
# Category theory.

object = Sort('object', [2])
arrow = Sort('arrow', [3])
sorts = [object, arrow]

id = Function('id', [object], arrow)
src = Function('src', [arrow], object)
tgt = Function('tgt', [arrow], object)
compose = PartialFunction('compose', [arrow, arrow], arrow)
funcs = [id, src, tgt, compose]

X = Variable('X', object)
Y = Variable('Y', object)
f = Variable('f', arrow)
g = Variable('g', arrow)
h = Variable('h', arrow)

theory = Theory([
    src(id(X))==X,
    tgt(id(X))==X,

    compose(id(X), f).exists().implies(compose(id(X), f) == f),
    compose(f, id(X)).exists().implies(compose(f, id(X)) == f),

    (src(g)==tgt(f)).implies(compose(f, g).exists()),
    (compose(f, g).exists()).implies(tgt(f)==src(g)),

    #(compose(f, g).exists() & compose(g, h).exists()).implies( # dont need this
    compose(f, compose(g, h)) == compose(compose(f, g), h),

    (src(g)==tgt(f)).implies(src(compose(f, g))==src(f)), 
    (src(g)==tgt(f)).implies(tgt(compose(f, g))==tgt(g)),
])


