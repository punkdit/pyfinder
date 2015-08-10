#!/usr/bin/env python

#import psyco
#psyco.full()

from expr import dummy

from search import crossiter, multirange, Search, MultiSearch, TreeSearch


class Refutations(object):
    null = True
    def __init__(self, theory, funcs, cells):
        self.theory = theory
        self.funcs = funcs

        # currently considered cell values
        self.cells = cells

    def push(self, cellindex, cellvalues):
        return cellvalues

    def choose(self, cellindex, value):
        self.cells[cellindex] = value

    def clear(self, cellindex):
        self.cells[cellindex] = None

    def add(self, refutation):
        pass

class ValueSearch(object):
    "search through values in a single cell"
    def __init__(self, db, cellindex, cellvalues):
        self.db = db # a Refutations instance
        self.cellindex = cellindex
        cellvalues = self.db.push(cellindex, cellvalues[:])
        self.cellvalues = iter(cellvalues)

    def next(self):
        value = self.cellvalues.next()
        self.db.choose(self.cellindex, value)

    def clear(self):
        self.db.clear(self.cellindex)


class Interpretation(object):
    debug = False

    def __init__(self, theory, funcs):
        self.theory = theory
        self.funcs = funcs
        self.cellspace = []
        index = 0
        for func in self.funcs:
            func.index = index
            index += len(func.domain())
            self.cellspace.extend([func.range() for _ in func.domain()])
        assert index == len(self.cellspace)
        if self.debug:
            print self.cellspace
        self.cells = [None] * len(self.cellspace)
        self.stack = []
        self.clauses = theory.clauses
        for clause in self.clauses:
            clause.init()
        self.db = Refutations(theory, funcs, self.cells)

    def __iter__(self):
        return self

    def validate(self, cells):
        for func in self.funcs:
            func.map = func.getmap(cells)
        for clause in self.clauses:
            valuations = crossiter([range(var.sort.size) for var in clause.vars])
            for valuation in valuations:
#                print clause.code()
                #print clause.code(), cells, valuation
                accept = clause.fastaccept(cells, *valuation)

                if 0:
                    _accept = clause.accepts(valuation)
                    assert accept == _accept

                if not accept:
                    indexs = clause.refutation(cells, *valuation)
                    refutation = list((index, cells[index]) for index in indexs)
                    refutation.sort()
                    if self.debug:
                        print clause
                        print clause.code(), ":"
                        print ' '.join('%s = %s' % (var.name, valuation[i]) for i, var in enumerate(clause.vars))
                        print cells
                        print clause.refutation_code()
                        print refutation
                        for func in clause.funcs:
                            _cells = [(cell if idx in indexs else None) for idx, cell in enumerate(cells)]
                            print func.tablestr(_cells)
                        print
                    return refutation
#            print
        return None

    def pop(self):
        self.stack.pop().clear()

    def push(self):
        cellindex = len(self.stack)
        self.stack.append(ValueSearch(self.db, cellindex, self.cellspace[cellindex]))

    def _next(self):
        while len(self.stack):
            try:
                self.stack[-1].next() # this sets a value in self.cells
                if self.debug: print "_next", self.cells
                return
            except StopIteration:
                self.cells[-1] = None
                self.pop()
        raise StopIteration

    def next(self):
        stack = self.stack
        while 1:
            if len(stack) < len(self.cells):
                self.push()
            self._next()
            #assert not None in self.cells[:len(stack)]
            if len(stack)==len(self.cells):
                refutation = self.validate(self.cells)
                if refutation is None:
                    break
                else:
                    self.db.add(refutation)
                    index, value = refutation[-1]
                    if index+1<len(self.stack):
                        while index+1<len(self.stack):
                            self.pop()
                        self._next()

            if not(self.stack):
                raise StopIteration
        return self.cells[:]

    def is_complete(self):
        return len(self.search) == len(self.cells)

    def __str__(self):
        return str(self.cells)


class Solver(object):
    def __init__(self, theory, sorts, funcs):
        self.theory = theory
        self.sorts = sorts
        self.funcs = funcs
        self.sizeiter = crossiter([s.sizes for s in sorts])

    def assign_sizes(self):
        for sizes in self.sizeiter:
            print
            # set the size of each sort
            for idx, size in enumerate(sizes):
                sorts[idx].size = size
                print "%s.size = %s"%(sorts[idx], size)
            yield None

    def solve(self):
        for _ in self.assign_sizes():
        
            positions = Interpretation(self.theory, self.funcs)
        
            count = 0
            for position in positions:
        
                print '_'*79
                print
                for func in self.funcs:
                    print func.tablestr(position)
                    print
                count += 1
        
            print "models found:", count


if __name__ == "__main__":
    import sys
    name = sys.argv[1]
    exec open(name)
    for arg in sys.argv[2:]:
        if '=' in arg:
            key, val = arg.split('=')
            val = int(val)
            globals()[key].sizes = [val]
    solver = Solver(theory, sorts, funcs)

    if 'profile' in sys.argv:
        import cProfile
        cProfile.run('solver.solve()')
    else:
        solver.solve()
    
    







