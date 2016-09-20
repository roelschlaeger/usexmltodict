# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/brackets/

from __future__ import print_function


import re


def checkio(s):
    """Check for matching bracket characters."""

    # isolate just the bracket characters
    s = list("".join(re.split('[^\(\)\{\}\[\]]', s)))

    stack = []
    for c in s:

        if c in "({[":
            stack.append(c)
            continue

        if len(stack):
            c2 = stack.pop()
            if (
                (c2 == "(" and c == ")") or
                (c2 == "[" and c == "]") or
                (c2 == "{" and c == "}")
            ):
                continue
            else:
                return False
        else:
            return False

    return len(stack) == 0

assert checkio("((5+3)*2+1)") == True
assert checkio("{[(3+1)+2]+}") == True
assert checkio("(3+{1-1)}") == False
assert checkio("[1+1]+(2*2)-{3/3}") == True
assert checkio("(({[(((1)-2)+3)-3]/3}-3)") == False
assert checkio("2+3") == True
