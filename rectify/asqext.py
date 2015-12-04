from collections import deque
from enum import Enum
from itertools import chain

from asq.extension import extend
from asq.indexedelement import IndexedElement
from asq.queryables import Queryable


@extend(Queryable)
def copy_padded_triples(self, selector=tuple):
    def generate_copy_padded_triple():
        w = deque(maxlen=3)
        i = iter(self)
        pad = next(i)
        w.append(pad)
        w.append(pad)
        for latest_item in i:
            w.append(latest_item)
            yield selector(w)
            pad = latest_item
        w.append(pad)
        yield selector(w)
    return Queryable(generate_copy_padded_triple())


@extend(Queryable)
def max_index(self, start=None, selector=IndexedElement):
    max_index = -1
    max_item = 0
    for index, item in enumerate(self, start=start):
        if item > max_item or max_index == -1:
            max_index = index
            max_item = item
    return IndexedElement(max_index, max_item)

