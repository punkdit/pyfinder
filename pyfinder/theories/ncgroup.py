#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Group theory.

element = Sort('element', size=6)

id = Constant(0, element) # arbitrarily fix this

A = Constant(1, element)
B = Constant(2, element)

inv = Function('inv', [element], element)
o = Function('o', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

theory = Theory([
    inv(inv(a)) == a,
    o(id, a) == a,
    o(a, id) == a,
    o(inv(a), a) == id,
    o(a, inv(a)) == id,
    o(a, o(b, c)) == o(o(a, b), c),
    o(A, B) != o(B, A),
])


sorts = [element]
funcs = [inv, o]



