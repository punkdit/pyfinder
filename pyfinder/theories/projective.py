#!/usr/bin/env python

from pyfinder.expr import *

#______________________________________________________________________________
# Finite projective geometry. Could not get this to produce any models. (Too big i think)

point = Sort('point')
line = Sort('line')

intersect = PartialFunction('I', [line, line], point)
join = PartialFunction('J', [point, point], line)
flag = Function('F', [point, line], BOOL)

sorts = [point, line]
funcs = [intersect, join, flag]
#funcs = [flag]

p1 = Variable('p1', point)
p2 = Variable('p2', point)
l1 = Variable('l1', line)
l2 = Variable('l2', line)

POINTS = [Constant(i, point) for i in range(4)]

exprs = [
    (p1==intersect(l1, l2)).implies(flag(p1, l1) & flag(p1, l2)),
    (l1==join(p1, p2)).implies(flag(p1, l1) & flag(p2, l1)),
    (flag(p1, l1) & flag(p1, l2) & (l1!=l2)).implies(intersect(l1, l2)==p1),
    (flag(p1, l1) & flag(p2, l1) & (p1!=p2)).implies(join(p1, p2)==l1),
    (l1!=l2) == (intersect(l1, l2).exists()),
    (p1!=p2) == (join(p1, p2).exists()),
]

#exprs = [
#    (l1!=l2).implies(flag(p1, l1) & flag(p1, l2)),
#    (p1!=p2).implies(flag(p1, l1) & flag(p2, l1)),
#    #((p1 != p2) & flag(p1, l1) & flag(p2, l1) & flag(p1, l2) & flag(p2, l2)).implies(l1==l2),
#    #((l1 != l2) & flag(p1, l1) & flag(p1, l2) & flag(p2, l1) & flag(p2, l2)).implies(p1==p2),
#]

for i in range(4):
  for j in range(i+1, 4):
    for k in range(4):
      if k!=i and k!=j:
        #e = (flag(POINTS[i], l1) & flag(POINTS[j], l1)).implies(flag(POINTS[k], l1) == false)
        #e = (flag(POINTS[i], l1) & flag(POINTS[j], l1) & flag(POINTS[k], l1)).implies(BOT)
        e = (flag(POINTS[i], l1) & flag(POINTS[j], l1)).implies(~flag(POINTS[k], l1))
        #e = (join(POINTS[i], POINTS[j])==l1).implies(~flag(POINTS[k], l1))
        exprs.append(e)
        #exprs.insert(0, e)

for e in exprs:
    print e
    
theory = Theory(exprs)




