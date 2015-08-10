#!/usr/bin/env python



class Node(object):
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.active = False
        self.prev = None
        self.next = None
        self.up = None

    def get_head(self):
        node = self
        while node.prev:
            node = node.prev
        return node

    def update_items(self, items):
        node = self.get_head()
        while node:
            if node.index in items:
                assert items[node.index] == node.value
            items[node.index] = node.value
            node = node.next


class Refutations(object):
    paranoid = False
    def __init__(self, cells):
        self.cells = cells
        size = len(cells)
        self.nodes = [None] * size
        self.idx = 0
        self.rows = [] # debug only
        self.all = set()

    def dump(self):
        for node in self.rows:
            print '\t',
            while node:
                print "(%s, %s, %s)" % (node.index, node.value, node.active),
                node = node.next
            print

    def add(self, refutation):
        #print "add", refutation
        refutation = tuple(refutation)
        if refutation in self.all:
            return
        self.all.add(refutation)
        prev = None
        node = None
        for index, value in refutation:
            node = Node(index, value)
            if not prev:
                self.rows.append(node)
            if (not prev or prev.active) and value == self.cells[index]:
                node.active = True
            node.prev = prev
            if prev:
                prev.next = node
            prev = node
            _node = self.nodes[index]
            self.nodes[index] = node
            node.up = _node
                
        node.next = None

    def push(self, index, values):
        node = self.nodes[index]
        nodes = []
        while node:
            if (not node.prev or node.prev.active) and node.next is None and node.value in values:
                values.remove(node.value)
                nodes.append(node)
            node = node.up
        if not values: 
#            return values
            # get secondary refutation
            items = {}
            for node in nodes:
                node = node.get_head()
                while node.index < index:
                    assert items.get(node.index) in (None, node.value)
                    items[node.index] = node.value
                    node = node.next
            items = items.items()
            if len(items)<8 or 1:
                items.sort()
                self.add(items)
        return values

    def check(self):
        #self.dump()
        for node in self.rows:
            assert node.prev is None
            while node:
                if node.next:
                    assert node.next.prev == node
                    assert node.next.index > node.index
                node = node.next
        for index, node in enumerate(self.nodes):
            value = self.cells[index]
            while node:
                assert node.index == index
                prev = node.prev
                if prev and not prev.active:
                    assert not node.active
                elif prev:
                    assert node.active == (node.value==value), (node.index, node.value, node.active, value)
                node = node.up
        #print "ok"

    def choose(self, index, value):
        #print "choose", index, value
        #print ' '*index+str(value)
        self.cells[index] = value
        node = self.nodes[index]
        while node:
            if (not node.prev or node.prev.active) and node.value == value:
                node.active = True
            else:
                node.active = False # only need this if we just backtracked
            node = node.up
        if self.paranoid:self.check()
        
    def clear(self, index):
        #print "clear", index
        #print ' '*index+'X'
        self.cells[index] = None
        node = self.nodes[index]
        while node:
            node.active = False
            node = node.up








