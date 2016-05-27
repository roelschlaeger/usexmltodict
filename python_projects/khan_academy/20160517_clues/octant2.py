"""Check SYMBOLS from octant.py"""

from __future__ import print_function

from octant import SYMBOLS


def line_check(row, symbols):

    out = []

    symbols = symbols.strip()

    if len(symbols) != 0:

        s = symbols

        if len(s) & 1:
            print("length error: ", row, len(s), s)

        col = 0

        while s:
            c1, c2, s = s[0], s[1], s[2:]

            n1 = int(c1)
            n2 = int(c2)

            if ((n1 ^ n2) & 1) == 0:
                print(row, col, n1, n2)

            # return results in (even, odd) order
            if n1 & 1:
                out.append((n2, n1))
            else:
                out.append((n1, n2))

            col += 2

    return out


def symbols_check():
    # symbols = "".join(SYMBOLS.split('\n'))
    result = []
    for row, line in enumerate(SYMBOLS.split('\n')):
        result.extend(line_check(row, line))
    return result


if __name__ == "__main__":

    from pprint import pprint

    result = symbols_check()
    pprint(result)

    from collections import Counter
    c = Counter(result)
    print(c)


# end of file

