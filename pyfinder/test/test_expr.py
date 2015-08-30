#!/usr/bin/env python

from pyfinder.expr import Sort, Variable, Function, BOOL, false, true


def test_request():
    element = Sort('element', size=3)
    v = Variable('v', element)
    func = Function('func', [element], element, index=0)
    e = func(v)
    count = 0
    for valuation, cellvalues in e.request(0):
        assert len(valuation) == 1
        value = valuation[v]
        assert cellvalues == {value:0}
        count += 1
    assert count == 3


"""
>>> from expr import *
>>> element = Sort('el', size=3)
>>> v = Variable('v', element)
>>> func = Function('func', [element], element, index=0)
>>> expr = func(v)
>>> func = Function('func', [element], element, index=0)
>>> expr = func(v)
>>> for valuation, cellvalues in e.request(0):
...   print valuation, cellvalues
... 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'e' is not defined
>>> for valuation, cellvalues in expr.request(0):
...   print valuation, cellvalues
... 
{Variable('v', Sort('el')): 0} {0: 0}
{Variable('v', Sort('el')): 1} {1: 0}
{Variable('v', Sort('el')): 2} {2: 0}
>>> 

"""





def test_request_2():
    element = Sort('element', size=3)
    v = Variable('v', element)
    func = Function('func', [element], element, index=0)
    e = func(v)==v

    count = 0
    for valuation, cellvalues in e.request(true):
        assert len(valuation) == 1
        value = valuation[v]
        assert cellvalues == {value:value}
        count += 1
    assert count == 3


def test_request_3():
    element = Sort('element', size=3)
    v = Variable('v', element)
    func = Function('func', [element], element, index=0)
    e = func(v)==v

    count = 0
    for valuation, cellvalues in e.request(false):
        assert len(valuation) == 1
        value = valuation[v]
        assert len(cellvalues) == 1
        assert cellvalues.keys() == [value]
        assert cellvalues[value] != value
        count += 1
    assert count == 6


def test_request_4():
    element = Sort('element', size=3)
    v = Variable('v', element)
    le = Function('le', [element, element], BOOL, index=0)

    e = le(v, v)

    count = 0
    for valuation, cellvalues in e.request(false):
        assert len(valuation) == 1
        value = valuation[v]
        assert len(cellvalues) == 1
        index = 3*value + value
        assert cellvalues.keys() == [index]
        assert cellvalues[index] == 0
        count += 1
    assert count == 3



