# coding=utf-8
"""Pairs of three-bit values used to XOR Polybius (row, col) values."""

from __future__ import print_function
from polybius6 import Polybius6

#   TRIBITS = [
#       (4, 3), (3, 2), (5, 4), (1, 5), (6, 0), (6, 2), (4, 2), (4, 2), (7, 2),
#       (0, 7), (6, 4), (3, 4), (0, 7), (4, 1), (0, 2), (4, 3), (6, 6), (3, 1),
#       (2, 0), (3, 2), (2, 5), (3, 0), (1, 5), (6, 1), (5, 2), (1, 0), (4, 2),
#       (5, 5), (4, 1), (3, 1), (2, 7), (3, 2), (6, 3), (2, 3), (4, 2), (6, 4),
#       (3, 1), (6, 0), (7, 2), (2, 5), (5, 0), (4, 0), (2, 3), (6, 2), (6, 6),
#       (1, 7), (0, 5), (4, 3), (3, 7), (3, 6), (4, 4), (4, 3), (0, 3), (4, 4),
#       (2, 1), (6, 3), (2, 2), (3, 7), (2, 0), (4, 0), (6, 2), (3, 7), (2, 0),
#       (2, 1), (1, 4), (5, 5), (1, 2), (3, 3), (6, 1), (4, 1), (3, 2), (4, 0),
#       (0, 5), (3, 7), (0, 1), (0, 7), (5, 4), (3, 1), (1, 2), (0, 5), (1, 3),
#       (5, 4), (7, 6), (3, 5), (4, 0), (4, 6), (6, 7), (0, 0), (6, 1), (5, 4),
#       (2, 4), (2, 3), (0, 4), (3, 1), (5, 0), (5, 4), (4, 0), (3, 2), (4, 7),
#       (5, 1), (1, 0), (5, 7), (4, 2), (2, 5), (6, 0), (4, 0)
#   ]

# Each entry in HEXBITS represents six bits extracted from the
# 9210801046_586c49b847_c.jpg image as described in dibits.py
# The entries in TRIBITS are the pairs of three-bit numbers used to generate
# each of the HEXBITS entries. For example, (4, 3) ==> 4 * 8 + 3 = 35.
# Each number represents one character.

HEXBITS = [
    35, 26, 44, 13, 48, 50, 34, 34, 58, 7, 52, 28, 7, 33, 2, 35, 54, 25, 16,
    26, 21, 24, 13, 49, 42, 8, 34, 45, 33, 25, 23, 26, 51, 19, 34, 52, 25, 48,
    58, 21, 40, 32, 19, 50, 54, 15, 5, 35, 31, 30, 36, 35, 3, 36, 17, 51, 18,
    31, 16, 32, 50, 31, 16, 17, 12, 45, 10, 27, 49, 33, 26, 32, 5, 31, 1, 7,
    44, 25, 10, 5, 11, 44, 62, 29, 32, 38, 55, 0, 49, 44, 20, 19, 4, 25, 40,
    44, 32, 26, 39, 41, 8, 47, 34, 21, 48, 32
]

# PAD is a transcription of the newspaper article found at the scene
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
Should you be scared if you own
a lot of these stocks either directly
or through mutual funds or
exchange-traded funds? David
Baskin, president of Baskin Finan-
cial Services, has a two-pronged
answer: Keep your top-quality
dividend stocks, but be prepared
to follow his firm's example in
trimming holdings in stucks such
as TransCanada Corp., Keyera
Corp. and Pembina Pipeline
Corp.
Let's have Mr. Baskin run us
through his thinking on dividend
stocks, which are a bit part of the
portfolios his firm puts together
for clients. A mini-manifesto
"""

PAD_CHARS = "".join([x for x in PAD.upper() if x.isalpha()])

# adjust length of PAD_CHARS to a multiple of 6
if (len(PAD_CHARS) % 6):
    PAD_CHARS += "Z" * (6 - (len(PAD_CHARS) % 6))

# print(len(PAD_CHARS))


def pad_mask(s, debug=False):
    s = list(s)

    def isvowel(c):
        if c in "AEIOUY":
            return 1
        return 0

    while s:
        out = 0
        for _ in range(6):
            c = s.pop(0)
            n = isvowel(c)
            out = out * 2 + n

            if debug:
                print(c, n, sep="", end=" ")

        if debug:
            print(end="\n")

        yield out

#   generator = pad_mask(PAD_CHARS, False)
#   while 1:
#       print(generator.next())

########################################################################


def decrypt_one_time_pad(pb, hexbits, pad_chars, debug=False):
    """Decrypt the tribits message using the one-time pad."""

    generator = pad_mask(PAD_CHARS)

    if debug:
        print("hexbits   length: ", len(hexbits))
        print("pad_chars length: ", len(pad_chars))
        print()

    print("idx   t  x  v n1 n2 c")
    print("---   -  -  -  -  - -")
    out = []
    for index, t in enumerate(hexbits):
        x = generator.next()
        v = t ^ x
        n1, n2 = divmod(v, 8)
        try:
            c = pb.polybius_char(n1, n2)
        except AssertionError:
            c = "?"
        if debug:
            print("%3d: %2d %2d %2d %2d %2d %c" % (index, t, x, v, n1, n2, c))
        out.append(c)
    return "".join(out)

########################################################################

if __name__ == '__main__':

    from pprint import pprint

    def printby(s, n):
        """Print the 's' string in 'n' character chunks."""
        out = []
        while s:
            t, s = s[:n], s[n:]
            out.append(t)
        pprint(out)

    # printby(PAD_CHARS, 6)
    generator = pad_mask(PAD_CHARS)
    # from dibits import binary6
    # pprint([(x, binary6(x)) for x in generator])
    # print()

    PB = Polybius6()
    key2 = "FGHIJK EXYZ0L DW781M CV692N BU543O ATSRQP"
    PB.set_key(key2)
    PB.print_polybius()
    cleartext = decrypt_one_time_pad(PB, HEXBITS, PAD_CHARS, True)
    print(cleartext)

# end of file
