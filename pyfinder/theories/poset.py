#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Poset theory.

element = Sort('element')

le = Function('le', [element, element], BOOL)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    le(a, a),
    (le(a, b) & le(b, c)).implies(le(a, c)),
    (le(a, b) & le(b, a)).implies(a==b),
])

sorts = [element]
funcs = [le]



