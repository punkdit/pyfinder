#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Category theory (arrows only).

element = Sort('element')
sorts = [element]

src = Function('src', [element], element)
tgt = Function('tgt', [element], element)
compose = PartialFunction('compose', [element, element], element)
funcs = [src, tgt, compose]

f = Variable('f', element)
g = Variable('g', element)
h = Variable('h', element)

theory = Theory([

    (src(g)==tgt(f)).implies(compose(f, g).exists()),
    (compose(f, g).exists()).implies(tgt(f)==src(g)),

    tgt(src(f))==src(f),
    src(tgt(f))==tgt(f),
    compose(src(f), f)==f,
    compose(f, tgt(f))==f,

    src(compose(f, g)) == src(compose(f, src(g))),
    tgt(compose(f, g)) == tgt(compose(tgt(f), g)),

    compose(f, compose(g, h)) == compose(compose(f, g), h),

    # put all the "identity" elements first
    src(f) <= f,
    tgt(f) <= f,
])

def test():
    element.size = 2
    src.index = 0
    tgt.index = 2
    compose.index = 4
    
    e = compose(f, tgt(f))
    e = tgt(src(f))==src(f)

#    e = tgt(src(f))
    e = src(f)
    for v,c in e.request(0):
        print '='*20, v, c, '='*20
        print


#test()


