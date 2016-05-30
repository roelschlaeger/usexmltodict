# coding=utf-8
"""Pairs of three-bit values used to XOR Polybius (row, col) values."""

from __future__ import print_function
from polybius6 import Polybius6
from dibits import binary6

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
    35, 58, 36, 15, 48, 18, 34, 34, 58, 5, 60, 60, 15, 35, 2, 33, 62, 59, 16,
    58, 29, 56, 5, 19, 42, 8, 34, 47, 33, 59, 31, 58, 51, 49, 34, 20, 25, 16,
    58, 55, 40, 32, 19, 18, 62, 13, 13, 33, 23, 62, 44, 33, 3, 36, 17, 17, 18,
    61, 16, 32, 50, 61, 16, 51, 4, 47, 10, 57, 49, 35, 26, 32, 13, 61, 1, 5,
    36, 59, 10, 7, 11, 44, 54, 63, 32, 38, 63, 0, 49, 44, 28, 49, 12, 59, 40,
    44, 32, 58, 47, 43, 8, 45, 34, 55, 48, 32
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
dend payers has stalled.
Should you be scared if you own
a lot of these stocks either directly
or through mutual funds or
exchange-traded funds? David
Baskin, president of Baskin Finan-
cial Services, has a two-pronged
answer: Keep your top-quality
dividend stocks, but be prepared
to follow his firm's example in
trimming holdings in stocks such
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
# if (len(PAD_CHARS) % 6):
#     PAD_CHARS += "Z" * (6 - (len(PAD_CHARS) % 6))

# print(len(PAD_CHARS))


def pad_mask(s, debug=False):
    """Compute 6-bit XOR masks from the string s."""
    s = list(s)
    exhausted = False

    def isvowel(c):
        """Return 1 for vowel, 0 otherwise."""
        if c in "AEIOUY":
            return 1
        return 0

    while s:
        out = 0
        for _ in range(6):
            try:
                c = s.pop(0)
            except IndexError:
                if not exhausted:
                    print("Input exhausted; padding with Z's")
                    exhausted = True
                c = "Z"
            n = isvowel(c)
            out = out * 2 + n

            if debug:
                print(c, n, sep="", end=" ")

        if debug:
            print(end="\n")

        yield out

    print("pad_mask exhausted; now returning 0's")

    while 1:
        yield 0

########################################################################


def print_pad_chars(s):
    """Display the results of pad_mask generation on string s."""
    print("idx   PAD  <-mask--> (binary and octal)")
    print("---  ------ ------ --")
    generator = pad_mask(s.upper())
    index = 0
    while s:
        t, s = s[:6], s[6:]
        n = generator.next()
        o = binary6(n)
        print("%3d %s %6s %02o " % (index, t, o, n))
        index += 1

print_pad_chars(PAD_CHARS)

########################################################################


def decrypt_one_time_pad(pb, hexbits, pad_chars, debug=False):
    """Decrypt the tribits message using the one-time pad."""
    generator = pad_mask(PAD_CHARS)

    if debug:
        print("hexbits   length: ", len(hexbits))
        print("pad_chars length: ", len(pad_chars))
        print()

    print("idx   t  x  v n1 n2 c (t x v are in octal)")
    print("---   -  -  -  -  - -")
    out = []
    for index, t in enumerate(hexbits):
        x = generator.next()
        v = t ^ x
        n1, n2 = divmod(v, 8)
        c = pb.polybius_char(n1, n2, alt="?")
        if debug:
            print("%3d: %02o %02o %02o %2d %2d %c"
                  % (index, t, x, v, n1, n2, c)
                  )
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

    key2 = "FGHIJK EXYZ0L DW781M CV692N BU543O ATSRQP"
    pb = Polybius6(key2, False)
    pb.print_polybius()
    print()
    cleartext = decrypt_one_time_pad(pb, HEXBITS, PAD_CHARS, True)
    print(cleartext)

# end of file
