# coding=utf-8
"""Pairs of three-bit values used to XOR Polybius (row, col) values."""

from __future__ import print_function
from polybius import Polybius5

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

########################################################################


def decrypt_one_time_pad(pb, tribits, pad_chars, debug=False):
    """Decrypt the tribits message using the one-time pad."""
    if debug:
        print("tribits   length: ", len(tribits))
        print("pad_chars length: ", len(pad_chars))
        print()

    out = []
    for index, t in enumerate(tribits):
        t1, t2 = t
        if debug:
            print(t1, t2)
        n1, n2 = pb.polybius_pair(pad_chars[index])
        if debug:
            print(n1, n2)
            print("----")
        n1 = n1 ^ t1
        n2 = n2 ^ t2
        if debug:
            print(n1, n2)
            print()
        out.append(pb.polybius_char(n1, n2))
    return "".join(out)

########################################################################

if __name__ == '__main__':

    # AFKPU
    # BGLQV
    # CHMRW
    # DINSX
    # EJOTY
    # key1 = "AFKPUBGLQVCHMRWDINSXEJOTY"

    # EJOTY
    # DINSX
    # CHMRW
    # BGLQV
    # AFKPU
    PB = Polybius5()
    key2 = "EJOTYDINSXCHMRWBGLQVAFKPU"
    PB.set_key(key2)
    PB.print_polybius()

#   print(PAD)
#   print(PAD_CHARS)

#   PAD_PAIRS = PB.text2pairs(PAD_CHARS)
#   from pprint import pprint
#   pprint(PAD_PAIRS, width=78)

    cleartext = decrypt_one_time_pad(PB, TRIBITS, PAD_CHARS, True)
    print(cleartext)

# end of file
