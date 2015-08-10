
# pyfinder

This is a constraint satisfaction solver based on
the [C implementation](http://users.cecs.anu.edu.au/~jks/finder.html) from John Slaney.
Finder is short for "Finite Domain Enumerator".

The idea is to specify a *theory* about a finite
sets of things, and functions on those things.

For example, group theory:

```
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
```

We can now look for examples of groups with
three elements:

```
$ ./solver3.py theories/group.py 

Sort('element').size = 3
_______________________________________________________________________________

 inv |
-----+---
   0 | 0
   1 | 2
   2 | 1

 o |  0  1  2
---+----------
 0 |  0  1  2
 1 |  1  2  0
 2 |  2  0  1

models found: 1

```






