#!/usr/bin/env python

# Categories with a terminal object.

from pyfinder.theories.cat import *

hom = PartialFunction("hom", [object, object], arrow)
funcs.append(hom)

theory.extend([
    src(hom(X,Y))==X,
    tgt(hom(X,Y))==Y,
])


T = Function("T", [], object) # terminal object
funcs.append(T)

theory.extend([
    hom(X, T()).exists(),
    ((src(f)==X) & (tgt(f)==T()) & (src(g)==X) & (tgt(g)==T())).implies(f==g),
#    T() <= X,
])




