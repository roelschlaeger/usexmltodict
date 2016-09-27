# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/digits-multiplication/

import operator


def checkio(n):
    """Return the product of the non-zero digits in the number n."""
    return reduce(operator.mul, map(int, [c for c in str(n) if c != "0"]))

assert checkio(123405) == 120
assert checkio(999) == 729
assert checkio(1000) == 1
assert checkio(1111) == 1
print("Done!")
