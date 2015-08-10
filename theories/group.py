#!/usr/bin/env python

from expr import *

#______________________________________________________________________________
# Group theory.

element = Sort('element', [3])

id = Constant(0, element) # arbitrarily fix this
inv = Function('inv', [element], element)
o = Function('o', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    o(id, a) == a,
    o(a, id) == a,
    o(inv(a), a) == id,
    o(a, inv(a)) == id,
    o(a, o(b, c)) == o(o(a, b), c),
])


sorts = [element]
funcs = [inv, o]



