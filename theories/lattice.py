#!/usr/bin/env python

from expr import *

#______________________________________________________________________________
# Lattice (as a POSET) theory.

element = Sort('element')

le = Function('le', [element, element], BOOL)
sup = Function('sup', [element, element], element)
inf = Function('inf', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    le(a, a),
    (le(a, b) & le(b, c)).implies(le(a, c)),
    (le(a, b) & le(b, a)).implies(a==b),

    le(a, sup(a, b)),
    le(b, sup(a, b)),

    (le(a, c) & le(b, c)).implies(le(sup(a, b), c)),

    le(inf(a, b), a),
    le(inf(a, b), b),

    (le(c, a) & le(c, b)).implies(le(c, inf(a, b))),
])

sorts = [element]
funcs = [le, sup, inf]



