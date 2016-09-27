# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

from __future__ import print_function

# https://py.checkio.org/mission/fizz-buzz/


def checkio(n):
    """Check for divisibility by 3, 5, 15 or other."""

    three = ((n % 3) == 0)
    five = ((n % 5) == 0)

    if three and five:
        return "Fizz Buzz"
    elif three:
        return "Fizz"
    elif five:
        return "Buzz"
    else:
        return str(n)


assert checkio(15) == "Fizz Buzz"
assert checkio(6) == "Fizz"
assert checkio(5) == "Buzz"
assert checkio(7) == "7"
print("Done!")
