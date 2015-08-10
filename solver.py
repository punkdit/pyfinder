#!/usr/bin/env python

#import psyco
#psyco.full()

from expr import dummy

from search import crossiter, multirange, Search, MultiSearch

def nstr(map, key):
    arg = map.get(key)
    if arg == dummy:
        return ''
    elif arg is None:
        return '?'
    return str(arg)

def nullopstr(name, map):
    lines = []
    n = max(len(name)+1, 3)
    lines.append('%s |' % name.rjust(n))
    lines.append('='*(n+5))
    key = ()
    lines.append('%s | %s' % (str('').rjust(n), nstr(map, key)))
    return '\n'.join(lines)

def unopstr(name, map):
    lines = []
    n = max(len(name)+1, 3)
    lines.append('%s |' % name.rjust(n))
    lines.append('='*(n+5))
    keys = map.keys()
    keys.sort()
    for key in keys:
        lines.append('%s | %s' % (str(key[0]).rjust(n), nstr(map, key)))
    return '\n'.join(lines)

def binopstr(name, map):
    keys = map.keys()
    lhs = set([k[0] for k in keys])
    lhs = list(lhs)
    lhs.sort()
    rhs = set([k[1] for k in keys])
    rhs = list(rhs)
    rhs.sort()
    lines = []
    n = len(name) + 1
    lines.append('%s | %s' % (
        name.rjust(n), ' '.join(str(arg).rjust(2) for arg in rhs)
    ))
    lines.append('='*(n+3+len(rhs)*3))
    for l in lhs:
        lines.append('%s | %s' % (
            str(l).rjust(n), ' '.join(nstr(map, (l,r)).rjust(2) for r in rhs)
        ))
    return '\n'.join(lines)


class Interpretation(Search):
    def __init__(self, func):
        self.func = func
        self.domain = func.domain()
        assert self.domain, (func, self.domain)
        searches = [Search(iter, func.range()) for element in self.domain]
        self.search = MultiSearch(searches)
        func.map = self.map = {}
        self.reset()

    def reset(self):
        self.search.reset()
        self.map.clear()

    def next(self):
        values = self.search.next()
        for idx, value in enumerate(values):
            self.map[self.domain[idx]] = value
        #return None # not used..

    def __repr__(self):
        return "Interpretation(%s, %s)"%(self.func, self.map)

    def __str__(self):
        if len(self.func.sorts)==0:
            return nullopstr(self.func.name, self.map)
        elif len(self.func.sorts)==1:
            return unopstr(self.func.name, self.map)
        elif len(self.func.sorts)==2:
            return binopstr(self.func.name, self.map)
        else:
            return repr(self)


if __name__ == "__main__":
    import sys
    name = sys.argv[1]
    exec open(name)
    for arg in sys.argv[2:]:
        if '=' in arg:
            key, val = arg.split('=')
            val = int(val)
            globals()[key].sizes = [val]
    
    for sizes in crossiter([s.sizes for s in sorts]):
    
        print
        # set the size of each sort
        for idx, size in enumerate(sizes):
            sorts[idx].size = size
            print "%s.size = %s"%(sorts[idx], size)
        #print [s.size for s in sorts]
    
        interps = [Interpretation(func) for func in funcs]
        positions = MultiSearch(interps)
    
    
        count = 0
        for position in positions:
    
            accept = True
            for clause in theory.clauses:
                valuations = crossiter([range(var.sort.size) for var in clause.vars])
                for valuation in valuations:
                    if not clause.accepts(valuation):
                        accept = False
                        break
                if not accept:
                    break
            if not accept:
                continue
    
            print '_'*79
            for interp in interps:
                print interp
                print
            count += 1
    
        print "models found:", count
    
    
    







