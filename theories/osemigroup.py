#!/usr/bin/env python

from expr import *

#______________________________________________________________________________
# Ordered Semi-group theory.

element = Sort('element')

o = Function('o', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    (a<=b).implies(o(a, c)<=o(b, c)),
    (a<=b).implies(o(c, a)<=o(c, b)),
    o(a, o(b, c)) == o(o(a, b), c),
])


sorts = [element]
funcs = [o]



