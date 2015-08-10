#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Lattice (as an algebraic) theory.

element = Sort('element')

sup = Function('sup', [element, element], element)
inf = Function('inf', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)


theory = Theory([
    sup(a, b)==sup(b, a),
    inf(a, b)==inf(b, a),

    sup(a, sup(b, c))==sup(sup(a, b), c),
    inf(a, inf(b, c))==inf(inf(a, b), c),

    sup(a, inf(a, b))==a,
    inf(a, sup(a, b))==a,
])

sorts = [element]
funcs = [sup, inf]



