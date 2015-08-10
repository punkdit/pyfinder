#!/usr/bin/env python

from expr import *

#______________________________________________________________________________
# Monoid theory.

element = Sort('element')

id = Constant(0, element) # arbitrarily fix this
o = Function('o', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    o(id, a) == a,
    o(a, id) == a,
    o(a, o(b, c)) == o(o(a, b), c),
])


sorts = [element]
funcs = [o]



