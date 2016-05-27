# coding=utf-8
"""Pairs of three-bit values used to XOR Polybius (row, col) values."""

from __future__ import print_function
from polybius import set_key, print_polybius, text2pairs

TRIBITS = [
    (4, 3), (3, 2), (5, 4), (1, 5), (6, 0), (6, 2), (4, 2), (4, 2), (7, 2),
    (0, 7), (6, 4), (3, 4), (0, 7), (4, 1), (0, 2), (4, 3), (6, 6), (3, 1),
    (2, 0), (3, 2), (2, 5), (3, 0), (1, 5), (6, 1), (5, 2), (1, 0), (4, 2),
    (5, 5), (4, 1), (3, 1), (2, 7), (3, 2), (6, 3), (2, 3), (4, 2), (6, 4),
    (3, 1), (6, 0), (7, 2), (2, 5), (5, 0), (4, 0), (2, 3), (6, 2), (6, 6),
    (1, 7), (0, 5), (4, 3), (3, 7), (3, 6), (4, 4), (4, 3), (0, 3), (4, 4),
    (2, 1), (6, 3), (2, 2), (3, 7), (2, 0), (4, 0), (6, 2), (3, 7), (2, 0),
    (2, 1), (1, 4), (5, 5), (1, 2), (3, 3), (6, 1), (4, 1), (3, 2), (4, 0),
    (0, 5), (3, 7), (0, 1), (0, 7), (5, 4), (3, 1), (1, 2), (0, 5), (1, 3),
    (5, 4), (7, 6), (3, 5), (4, 0), (4, 6), (6, 7), (0, 0), (6, 1), (5, 4),
    (2, 4), (2, 3), (0, 4), (3, 1), (5, 0), (5, 4), (4, 0), (3, 2), (4, 7),
    (5, 1), (1, 0), (5, 7), (4, 2), (2, 5), (6, 0), (4, 0)
]

# EJOTY
# DINSX
# CHMRW
# BGLQV
# AFKPU
key2 = "EJOTYDINSXCHMRWBGLQVAFKPU"
set_key(key2)
print_polybius()

PAD = """
The whole grain goodness of
blue chip dividend stocks has
its limits.
Utility stocks, consumer staples,
pipelines, telecoms and real
estate investment trusts have all
lost ground over the past month,
even while the broader market
has been flat. With the bond mar-
ket signalling an expectation of
rising interest rates, the five-year
rally for steady blue-chip divi-
dend payers has been stalled.
"""

PAD_CHARS = "".join([x for x in PAD.upper() if x.isalpha()])


if __name__ == '__main__':

    from pprint import pprint

    print(PAD)
    print(PAD_CHARS)

    PAD_PAIRS = text2pairs(PAD_CHARS)
    pprint(PAD_PAIRS, width=78)
# end of file
