# vim:ts=4:sw=4:tw=0:wm=0:et

from __future__ import print_function
from collections import Counter

def checkio(s):
    c = Counter(s).most_common()
    for v, count in c:
        if count == 1:
            s.remove(v)
    return s

assert checkio([1, 2, 3, 1, 3]) == [1, 3, 1, 3]
assert checkio([1, 2, 3, 4, 5]) == []
assert checkio([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5]
assert checkio([10, 9, 10, 10, 9, 8]) == [10, 9, 10, 10, 9]
