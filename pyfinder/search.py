#!/usr/bin/env python


def crossiter(sets, verbose=False):
    sets = list(sets)
    if not sets:
        if verbose:print "XITER --->"
        yield ()
    elif len(sets)==1:
        for item in sets[0]:
            if verbose:print "XITER --->"
            yield (item,)
    else:
        for item in sets[0]:
            for rest in crossiter(sets[1:]):
                if verbose:print "XITER --->"
                yield (item,) + rest


def search(keys, n=5):
    if len(keys)==1:
        for i in range(n):
            yield (i,)
    else:
        for rest in search(keys[1:], n):
            for i in range(n):
                yield (i,) + rest


def multirange(ns):
    if len(ns)==1:
        for i in range(ns[0]):
            yield (i,)
    else:
        for rest in multirange(ns[1:]):
            for i in range(ns[0]):
                yield (i,) + rest


class Search(object):
    def __init__(self, func, *args):
        self.func = func
        self.args = args
        self.reset()

    def __iter__(self):
        return self

    def reset(self):
        assert type(self.args)==tuple, self.args
        self.gen = self.func(*self.args)

    def next(self):
        return self.gen.next()


class MultiSearch(Search):
    def __init__(self, searches):
        self.searches = searches
        self.reset()
        self.idx = 0

    def reset(self):
        for s in self.searches:
            s.reset()
        self.items = [s.next() for s in self.searches]
        self.idx = 0

    def next(self):
        if not self.items:
            raise StopIteration
        items = self.items[:]
        searches = self.searches
        while self.idx < len(searches):
            try:
                self.items[self.idx] = searches[self.idx].next()
                self.idx = 0
                return items
            except StopIteration:
                searches[self.idx].reset() # carry
                self.items[self.idx] = searches[self.idx].next()
                self.idx += 1
        self.items = None # raise next time..
        return items


class TreeSearch(Search):
    def __init__(self, searches, validator=None):
        self.searches = searches
        self.validator = validator
        self.reset()

    def reset(self):
        for s in self.searches:
            s.reset()
        self.idx = 0
        self.stack = [None for s in self.searches]

    def pop(self):
        self.searches[self.idx].reset()
        self.stack[self.idx] = None
        self.idx -= 1

    def next(self):
        stack = self.stack
        while self.idx>=0:
            try:
                while 1:
                    item = self.searches[self.idx].next()
                    stack[self.idx] = item
#                    if not self.validator or self.validator(stack):
                    self.idx = min(len(self.searches)-1, self.idx+1) # DFS
                    return stack[:] # clone
            except StopIteration:
                self.pop()
        raise StopIteration

    def is_leaf(self):
        return self.stack[-1] is not None


