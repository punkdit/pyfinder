
# pyfinder

This is a constraint satisfaction solver based on
the [C implementation](http://users.cecs.anu.edu.au/~jks/finder.html) from John Slaney.
Finder is short for "Finite Domain Enumerator".

The idea is to specify a `Theory` about finite
sets of things, and functions on those things.
Each such thing will come from a `Sort` with a
specified size.

For example, group theory:

```python
from pyfinder.expr import *

# Look for groups with 3 elements
element = Sort('element', 3)

# The identity element is a constant
# (which we arbitrarily fix to be 0)
id = Constant(0, element)

# Inverse is a unary function
inv = Function('inv', [element], element)

# Composition is a binary function
o = Function('o', [element, element], element)

a = Variable('a', element)
b = Variable('b', element)
c = Variable('c', element)

# Our theory is a list of equations that must be satisfied.
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

Here we have found there is only one group of size 3,
and it is the group of integers (under addition) modulo 3.

See also [Mace4](https://www.cs.unm.edu/~mccune/mace4/)
which is the state of the art in searching for these kinds
of finite algebraic models.



