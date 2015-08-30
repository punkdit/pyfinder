#!/usr/bin/env python

from search import crossiter


class Sort(object):
    def __init__(self, name, size=3):
        self.name = name
        self.sizes = [size]
        self.size = size
    def __repr__(self):
        return "Sort(%s)"%repr(self.name)
    __str__ = __repr__

dummy = -1
BOOL = Sort('BOOL', size=2)
false = 0
true = 1


class Expr(object):
    def __init__(self, sort):
        self.sort = sort

    def __eq__(self, other):
        return EqExpr(self, other)

    def __ne__(self, other):
        return NotExpr(EqExpr(self, other))

    def __and__(self, other):
        return AndExpr(self, other)

    def __neg__(self):
        return NotExpr(self)

    def __or__(self, other):
        return OrExpr(self, other)

    def __le__(self, other):
        return LEExpr(self, other)

    def exists(self):
        return ExistsExpr(self)

    def search(self):
        yield self

    def implies(self, other):
        clause = Clause([self], [other])
        return clause

    def evaluate(self, map):
        assert False


class NotExpr(Expr):
    def __init__(self, expr):
        assert expr.sort == BOOL
        Expr.__init__(self, BOOL)
        self.expr = expr

    def search(self):
        for expr in self.expr.search():
            yield expr
        yield self

    def __str__(self):
        return '~(%s)'%(self.expr,)

    def request(self, value):
        for result in self.expr.request(not value):
            yield result

    def evaluate(self, map):
        return not self.expr.evaluate(map)

    def code(self):
        return '(not %s)'%(self.expr.code(),)



def unify(a, b):
    for key, value in a.iteritems():
        _value = b.get(key)
        if _value is not None and _value != value:
            return None
    for key, value in b.iteritems():
        _value = a.get(key)
        if _value is not None and _value != value:
            return None
        a[key] = value
    return a


class BinExpr(Expr):
    def __init__(self, lhs, rhs):
        assert lhs.sort == rhs.sort, (lhs, rhs)
        Expr.__init__(self, BOOL)
        self.lhs = lhs
        self.rhs = rhs

    def search(self):
        for expr in self.lhs.search():
            yield expr
        for expr in self.rhs.search():
            yield expr
        yield self

    def __repr__(self):
        return "%s(%s, %s)"%(self.__class__.__name__, self.lhs, self.rhs)

    def __str__(self):
        return '(%s %s %s)'%(self.lhs, self.op, self.rhs)

    def request(self, value):
        for a in range(self.lhs.sort.size):
            for b in range(self.rhs.sort.size):
                if self.call(a, b)==bool(value):
#                    print "lhs=%s, rhs=%s"%(a, b)
                    for valuation, cellmap in self.lhs.request(a):
#                        print "lhs:", valuation, cellmap
                        for _valuation, _cellmap in self.rhs.request(b):
#                            print "  rhs:", _valuation, _cellmap
                            __valuation = unify(dict(valuation), _valuation)
                            if __valuation is None:
                                continue
                            __cellmap = unify(dict(cellmap), _cellmap)
                            if __cellmap is None:
                                continue
#                            print "    unify:", __valuation, __cellmap
                            yield __valuation, __cellmap


class EqExpr(BinExpr):
    op = '=='
    def __init__(self, lhs, rhs):
        assert lhs.sort == rhs.sort, (lhs, rhs)
        BinExpr.__init__(self, lhs, rhs)

    def evaluate(self, map):
        return self.lhs.evaluate(map) == self.rhs.evaluate(map)

    def code(self):
        return '(%s == %s)'%(self.lhs.code(), self.rhs.code())

    def call(self, a, b):
        return a==b


class AndExpr(BinExpr):
    op = 'and'
    def __init__(self, lhs, rhs):
        assert lhs.sort == BOOL and rhs.sort == BOOL, (lhs.sort, rhs.sort)
        BinExpr.__init__(self, lhs, rhs)

    def evaluate(self, map):
        return self.lhs.evaluate(map) and self.rhs.evaluate(map)

    def code(self):
        return '(%s and %s)'%(self.lhs.code(), self.rhs.code())

    def call(self, a, b):
        return a and b


class OrExpr(BinExpr):
    op = 'or'
    def __init__(self, lhs, rhs):
        assert lhs.sort == BOOL
        assert rhs.sort == BOOL
        BinExpr.__init__(self, lhs, rhs)

    def evaluate(self, map):
        return self.lhs.evaluate(map) or self.rhs.evaluate(map)

    def code(self):
        return '(%s or %s)'%(self.lhs.code(), self.rhs.code())

    def call(self, a, b):
        return a or b


class LEExpr(BinExpr):
    op = '<='
    def __init__(self, lhs, rhs):
        assert lhs.sort == rhs.sort, (lhs, rhs)
        BinExpr.__init__(self, lhs, rhs)

    def evaluate(self, map):
        return self.lhs.evaluate(map) <= self.rhs.evaluate(map)

    def code(self):
        return '(%s <= %s)'%(self.lhs.code(), self.rhs.code())

    def call(self, a, b):
        return a<=b


class ExistsExpr(Expr):
    def __init__(self, expr):
        Expr.__init__(self, BOOL)
        assert isinstance(expr, Application)
        assert expr.func.partial
        self.expr = expr

    def search(self):
        for expr in self.expr.search():
            yield expr
        yield self

    def __repr__(self):
        return "ExistsExpr(%s)"%self.expr

    def evaluate(self, map):
        return self.expr.evaluate(map) != dummy

    def code(self):
        return '(%s != %s)'%(self.expr.code(), dummy)

    def __str__(self):
        return 'E:%s'%self.expr

    def request(self, value):
        if not value:
            for result in self.expr.request(dummy):
                yield result
        else:
            for a in range(self.expr.sort.size):
                for result in self.expr.request(a):
                    yield result


class Variable(Expr):
    def __init__(self, name, sort=None):
        Expr.__init__(self, sort)
        self.name = name
        self.sort = sort

    def __repr__(self):
        return "Variable(%r, %s)"%(self.name, self.sort)

    def __str__(self):
        return self.name

    def evaluate(self, map):
        return map[self]

    def code(self):
        return self.name

    def request(self, value):
        # generate pairs (valuation, cellmap)
        yield {self:value}, {}


class Constant(Expr):
    def __init__(self, const, sort=None):
        Expr.__init__(self, sort)
        self.const = const
        self.sort = sort

    def __repr__(self):
        return "Constant(%r, %s)"%(self.const, self.sort)

    def __str__(self):
        return str(self.const)

    def evaluate(self, map):
        return self.const

    def code(self):
        return str(self.const)

    def request(self, value):
        # generate pairs (valuation, cellmap)
        if self.const == value:
            yield {}, {}


class Application(Expr):
    def __init__(self, func, args):
        Expr.__init__(self, func.result)
        self.func = func
        self.args = args

    def search(self):
        for arg in self.args:
            for expr in arg.search():
                yield expr
        yield self

    def __repr__(self):
        return "Application(%s, %s)"%(self.func, self.args)

    def __str__(self):
        return "%s(%s)"%(self.func, ', '.join(str(expr) for expr in self.args))

    def evaluate(self, map):
        # map: var -> index into sort
        values = tuple(arg.evaluate(map) for arg in self.args)
        if dummy in values:
            return dummy
        return self.func.map[values]

    def code(self):
        return self.func.code(self.args)

    def refutation_code(self):
        return self.func.refutation_code(self.args)

    def request(self, value):
        # generate pairs (valuation, cellmap)
        for result in self.func.request(self.args, value):
            yield result

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
    lines.append('-'*n+'-+---')
    key = ()
    lines.append('%s | %s' % (str('').rjust(n), nstr(map, key)))
    return '\n'.join(lines)

def unopstr(name, map):
    keys = map.keys()
    keys.sort()
    lines = []
    n = max(len(name)+1, 3)
    k = 2 if len(keys)<=10 else 3
    lines.append('%s | %s' % (
        " "*n, ' '.join(str(key[0]).rjust(k) for key in keys)
    ))
    s = '-' + '-'*k
    lines.append('-'*n+'-+-'+s*len(keys))
    lines.append('%s | %s' % (
        name.rjust(n), ' '.join(nstr(map, key).rjust(k) for key in keys)
    ))
    return '\n'.join(lines)

def binopstr(name, map):
    keys = map.keys()
    lhs = set([k[0] for k in keys])
    lhs = list(lhs)
    lhs.sort()
    rhs = set([k[1] for k in keys])
    rhs = list(rhs)
    rhs.sort()
    k = 2 if len(rhs)<=10 else 3
    lines = []
    n = len(name) + 1
    lines.append('%s | %s' % (
        name.rjust(n), ' '.join(str(arg).rjust(k) for arg in rhs)
    ))
    s = '-' + '-'*k
    lines.append('-'*n+'-+-'+s*len(rhs))
    for l in lhs:
        lines.append('%s | %s' % (
            str(l).rjust(n), ' '.join(nstr(map, (l,r)).rjust(k) for r in rhs)
        ))
    return '\n'.join(lines)


class Function(object):
    def __init__(self, name, sorts, result, **attr):
        self.name = name
        self.sorts = sorts
        self.arity = len(sorts)
        self.result = result
        self.injective = False
        self.canonical = False
        self.map = None # set by Interpretation
        self.index = None # set by Interpretation
        self.__dict__.update(attr)

    def __call__(self, *args):
        for idx, arg in enumerate(args):
            assert arg.sort == self.sorts[idx]
        return Application(self, args)

    def __repr__(self):
        return "%s(%r)"%(self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    def domain(self):
        items = list(crossiter(range(sort.size) for sort in self.sorts))
        return items

    def range(self):
        return range(self.result.size)

    def code(self, args):
        assert len(args) == self.arity
        if self.arity == 0:
            result = 'values[%s]' % self.index # XX rename values as cells
        elif self.arity == 1:
            result = 'values[%s + %s]' % (self.index, args[0].code()) # XX rename values as cells
        elif self.arity == 2:
            result = 'values[%s + %s*%s + %s]' % ( # XX rename values as cells
                self.index, self.sorts[0].size, args[1].code(), args[0].code())
        else:
            raise NotImplementedError
        return result

    def refutation_code(self, args):
        assert len(args) == self.arity
        if self.arity == 0:
            result = str(self.index)
        elif self.arity == 1:
            result = '%s + %s' % (self.index, args[0].code())
        elif self.arity == 2:
            result = '%s + %s*%s + %s' % (
                self.index, self.sorts[0].size, args[1].code(), args[0].code())
        else:
            raise NotImplementedError
        return result

    def getmap(self, cells):
        map = {}
        if self.arity == 0:
            map[()] = cells[self.index]
        elif self.arity == 1:
            for i in range(self.sorts[0].size):
                map[(i,)] = cells[self.index + i]
        elif self.arity == 2:
            for i in range(self.sorts[0].size):
                for j in range(self.sorts[1].size):
                    map[(i,j)] = cells[self.index + i + j*self.sorts[0].size]
        else:
            raise NotImplementedError
        return map

    def get_cellindex(self, args):
        assert self.arity == len(args)
        if self.arity == 0:
            index = self.index
        elif self.arity == 1:
            index = self.index + args[0]
        elif self.arity == 2:
            index = self.index + args[0] + args[1]*self.sorts[0].size
        else:
            raise NotImplementedError
        return index

    def tablestr(self, cells):
        self.map = self.getmap(cells)
        if self.arity == 0:
            return nullopstr(self.name, self.map)
        elif self.arity == 1:
            return unopstr(self.name, self.map)
        elif self.arity == 2:
            return binopstr(self.name, self.map)
        else:
            return repr(self)

    def request(self, args, value0):
        # generate pairs (valuation, cellmap)
        # XX we should pass valuation and cellmap around and let subexprs unify... XX
        #print self, "request", value0
        for valuation0 in crossiter(range(sort.size) for sort in self.sorts):
            #print "%s%s"%(self, valuation0)
            # Note: we unroll the request generators using list constructor (otherwise crossiter wont work):
            pairss = [list(args[i].request(value)) for (i, value) in enumerate(valuation0)]
            for result in crossiter(pairss):
                #print self, "unify: %s"%str(result)
                # try and unify result into single valuation, cellmap
                valuation, cellmap = {}, {}
                for _v, _c in result:
                    valuation = unify(valuation, _v)
                    if valuation is None:
                        #print self, "BAD valuation", self, '\n'
                        break
                    cellmap = unify(cellmap, _c)
                    if cellmap is None:
                        #print self, "BAD cellmap", self, '\n'
                        break
                if valuation is not None and cellmap is not None:
                    cellindex = self.get_cellindex(valuation0)
                    #print self, "valuation=%s, cellmap=%s"%(valuation, cellmap)
                    #print self, "valuation0=%s, cellindex=%d" % (valuation0, cellindex)
                    if not cellindex in cellmap or cellmap[cellindex] == value0:
                        cellmap[cellindex] = value0
                        #print self, "--->", valuation, cellmap
                        yield valuation, cellmap


class PartialFunction(Function):
    partial = True

    def range(self):
        return range(self.result.size) + [dummy]

    def code(self, args):
        assert len(args) == self.arity
        if self.arity == 0:
            result = 'values[%s]' % self.index # XX rename values as cells
        elif self.arity == 1:
            result = '(dummy if %s==dummy else values[%s + %s])' % ( # XX rename values as cells
                args[0].code(), self.index, args[0].code())
        elif self.arity == 2:
            result = '(dummy if (%s==dummy or %s==dummy) else values[%s + %s*%s + %s])' % ( # XX rename values as cells
                args[0].code(), args[1].code(),
                self.index, self.sorts[0].size, args[1].code(), args[0].code())
        else:
            raise NotImplementedError
        return result


class Clause(object):
    def __init__(self, antecedents, consequents):
        self.antecedents = antecedents
        for expr in antecedents:
            assert isinstance(expr, Expr), expr
            assert expr.sort == BOOL

        self.consequents = consequents
        for expr in consequents:
            assert isinstance(expr, Expr)
            assert expr.sort == BOOL

        vars = set()
        funcs = set()
        apps = set()
        self.slots = 0
        for expr in self.search():
            if isinstance(expr, Variable):
                vars.add(expr)
            elif isinstance(expr, Application):
                apps.add(expr)
                funcs.add(expr.func)
                self.slots += len(expr.func.sorts)
        self.vars = list(vars)
        self.funcs = list(funcs)
        self.apps = list(apps)

    def init(self):
        self.fastaccept = eval(self.code())
        self.refutation = eval(self.refutation_code())

    def search(self):
        for expr in self.antecedents + self.consequents:
            for _expr in expr.search():
                yield _expr

    def accepts(self, valuation):
        map = dict(zip(self.vars, valuation))
        for expr in self.antecedents:
            if not expr.evaluate(map):
                return True
        for expr in self.consequents:
            if expr.evaluate(map):
                return True
        return False

    def gen_refutations(self):
        valuation, cellmap = {}, {}
        if len(self.antecedents) == 0 and len(self.consequents) == 1:
            for _, cellmap in self.consequents[0].request(0):
                refutation = cellmap.items()
                refutation.sort()
                yield refutation
        elif len(self.antecedents) == 1 and len(self.consequents) == 1:
            expr = (-self.antecedents[0]) | self.consequents[0]
            for _, cellmap in expr.request(0):
                refutation = cellmap.items()
                refutation.sort()
                yield refutation

    def refutation_code(self):
        code = 'set((%s))'%(' '.join(app.refutation_code()+',' for app in self.apps))
        func = 'lambda values, %s: %s' % (', '.join(var.name for var in self.vars), code) # XX rename values as cells
        return func

    def code(self):
        antecedent = ' and '.join(expr.code() for expr in self.antecedents)
        consequent = ' or '.join(expr.code() for expr in self.consequents)
        s_vars = ', '.join(var.name for var in self.vars)
        if not antecedent:
            result = 'lambda values, %s: (%s)' % (s_vars, consequent) # XX rename values as cells
        elif not consequent:
            result = 'lambda values, %s: not (%s)' % (s_vars, antecedent) # XX rename values as cells
        else:
            result = 'lambda values, %s: (not (%s) or (%s))' % (s_vars, antecedent, consequent) # XX rename values as cells
        return result

    def __str__(self):
        return "%s -> %s" % (
            ', '.join(str(expr) for expr in self.antecedents), ', '.join(str(expr) for expr in self.consequents))


class Theory(object):
    def __init__(self, clauses):
        self.clauses = []
        self.extend(clauses)

    def extend(self, clauses):
        for item in clauses:
            self.append(item)

    def append(self, item):
        if isinstance(item, Expr):
            clause = Clause([], [item])
        else:
            clause = item
        self.clauses.append(clause)

    def search(self):
        for clause in self.clauses:
            for expr in clause.search():
                yield expr

    def all_sorts(self):
        sorts = set()
        for expr in self.search():
            sorts.add(expr.sort)
        if BOOL in sorts:
            sorts.remove(BOOL)
        return sorts

    def all_funcs(self):
        funcs = set()
        for expr in self.search():
            if isinstance(expr, Application):
                funcs.add(expr.func)
        return funcs

