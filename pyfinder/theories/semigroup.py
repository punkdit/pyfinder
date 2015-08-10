#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Semi-group theory.

element = Sort('element')

o = Function('o', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    o(a, o(b, c)) == o(o(a, b), c),
])


sorts = [element]
funcs = [o]



