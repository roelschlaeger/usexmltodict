# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-
# https://py.checkio.org/mission/pawn-brotherhood/

"""Determine which pawns are defended"""

columns = "abcdefgh"


def defenders(p):
    """Create list of possible defenders for a given pawn."""
    result = []
    c, r = columns.index(p[0]), int(p[1])
    if (r > 1):
        if c >= 1:
            result.append("%c%d" % (columns[c - 1], r - 1))
        if c < 7:
            result.append("%c%d" % (columns[c + 1], r - 1))
    return result


def safe_pawns(s):
    """Determine which pawns are defended."""

    count = 0
    for p in s:
        for defender in defenders(p):
            if defender in s:
                count += 1
                break
    return count

assert safe_pawns({"b4", "d4", "f4", "c3", "e3", "g5", "d2"}) == 6
assert safe_pawns({"b4", "c4", "d4", "e4", "f4", "g4", "e5"}) == 1
print("Done!")
