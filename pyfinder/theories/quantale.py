#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# 

element = Sort('element')
rig = Sort('rig')

TOP = I = Constant(0, element)
L = Constant(1, element)
P = Constant(2, element)
LP = Constant(3, element)
PL = Constant(4, element)
BOT = PLP = LPL = Constant(5, element)

mul = Function('mul', [element, element], element)

size = Function('size', [element], rig)

rzero = Constant(0, rig)
rone = Constant(1, rig)
radd = Function('radd', [rig, rig], rig)
rmul = Function('rmul', [rig, rig], rig)



a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

x = Variable('x', rig)
y = Variable('y', rig)
z = Variable('z', rig)

theory = Theory([
    mul(I, a) == a,
    mul(a, I) == a,
    mul(BOT, a) == BOT,
    mul(a, BOT) == BOT,
    mul(a, a) == a,
    mul(L, P) == LP,
    mul(P, L) == PL,
    mul(L, LP) == LP,
    mul(LP, P) == LP,
    mul(P, PL) == PL,
    mul(PL, L) == PL,
    mul(P, LP) == PLP,
    mul(L, PL) == LPL,
    mul(PL, P) == PLP,
    mul(LP, L) == LPL,
    mul(PL, LP) == BOT,
    mul(LP, PL) == BOT,
    radd(rzero, x) == x,
    rmul(rone, x) == x,
    rmul(x, rone) == x,
    rmul(x, rzero) == rzero,
    rmul(rzero, x) == rzero,
    radd(x, radd(y, z)) == radd(radd(x, y), z),
    rmul(x, rmul(y, z)) == rmul(rmul(x, y), z),
    radd(x, y) == radd(y, x),
    rmul(x, radd(y, z)) == radd(rmul(x, y), rmul(x, z)),
    rmul(radd(x, y), z) == radd(rmul(x, z), rmul(y, z)),
    size(I) == rone,
    size(LPL) == rzero,
    size(L)==size(P),
    size(LP)==size(PL),
    size(mul(a, b)) == rmul(size(a), size(b)),
    size(L)==Constant(2, rig),
])

sorts = [element, rig]
funcs = [mul, radd, rmul, size]



