"""Check SYMBOLS from octant.py"""

from __future__ import print_function

from octant import SYMBOLS


def line_check(row, symbols):

    out = []

    def save_bits(n1, n2):
        #               1             0
        # adjust n1    \|/            |
        #            7--.--3 ==>  2 --.-- 1
        #              /|\            |
        #               5             2
        #
        # adjust n2   8   2         2   1
        #              \|/           \ /
        #             --.--  ==>      .
        #              /|\           / \
        #             6   4         3   0

        assert n1 & 1, "n1 Error"
        assert (n2 & 1) == 0, "n2 Error"

        b1 = (n1 - 1) // 2
        b2 = (4 - n2) // 2 % 4
        assert 0 <= b1 <= 3, "b1 Error"
        assert 0 <= b2 <= 3, "b2 Error"
        out.append((b1, b2))

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
                save_bits(n1, n2)
            else:
                save_bits(n2, n1)

            col += 2

    return out


def symbols_check():
    # symbols = "".join(SYMBOLS.split('\n'))
    result = []
    for row, line in enumerate(SYMBOLS.split('\n')):
        result.extend(line_check(row, line))
    return result


DIBIT_PAIRS = symbols_check()

if __name__ == "__main__":

    from pprint import pprint

    pprint(DIBIT_PAIRS, width=29, compact=True)

    from collections import Counter
    c = Counter(DIBIT_PAIRS)
    print(len(c), "\n", c)


# end of file
