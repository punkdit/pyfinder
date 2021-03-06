#!/usr/bin/env python

#try:
#    import psyco
#    psyco.full() # runs twice as fast.
#except ImportError:
#    pass

from expr import dummy

from pyfinder.search import crossiter, multirange, Search, MultiSearch, TreeSearch
from pyfinder.refute import Refutations
from pyfinder.util import write


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
        #print self.cellspace
        self.cells = [None] * len(self.cellspace)
        self.stack = []
        self.clauses = theory.clauses
        for clause in self.clauses:
            clause.init()
        self.db = Refutations(self.cells)
        self.gen_small_refutations()

    def __iter__(self):
        return self

    debug = False
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

    def gen_small_refutations(self, size=5):
        if self.debug:
            print "clause slots:", [clause.slots for clause in self.clauses]
        clauses = [clause for clause in self.clauses if clause.slots < size]

        count = 0
        for clause in clauses:
            if self.debug:
                print "removing: (%s)" % clause
            for refutation in clause.gen_refutations():
                #print '\t', refutation
                self.db.add(refutation)
                count += 1
            self.clauses.remove(clause)
        if self.debug:
            print "gen_small_refutations: found %d refutations" % count

    def pop(self):
        self.stack.pop().clear()
        #write("B")

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
            #print
            # set the size of each sort
            for idx, size in enumerate(sizes):
                self.sorts[idx].size = size
                #print "%s.size = %s"%(self.sorts[idx], size)
            yield None

    def solve(self, max_count=0, verbose=True):

        for _ in self.assign_sizes():
        
            positions = Interpretation(self.theory, self.funcs)
        
            count = 0
            for position in positions:
        
                if verbose: 
                    print
                    print '_'*79
                    print position
                    print
                    for func in self.funcs:
                        print func.tablestr(position)
                        print
                else:
                    yield position
                count += 1
                if max_count and count>=max_count:
                    break
        
            if verbose:
                print "models found:", count


if __name__ == "__main__":
    from pyfinder.argv import argv
    name = argv.next()
    verbose = True
    exec open(name)
    for sort in sorts:
        size = argv.get(sort.name)
        if size:
            sort.sizes = [size]

    Interpretation.debug = argv.debug
    max_count = argv.get("max_count", 1)

    solver = Solver(theory, sorts, funcs)

    if argv.profile:
        import cProfile
        cProfile.run('list(solver.solve(max_count=max_count, verbose=verbose))')
    else:

        for _ in solver.solve(max_count=max_count, verbose=verbose):
            pass
    
    







