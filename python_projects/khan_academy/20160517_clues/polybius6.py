# coding=utf-8

"""Perform Polybius encoding using 6x6 matrix."""

from __future__ import print_function
from pprint import pprint
import string


class Polybius6(object):
    """A class supporting 6x6 Polybius cipher arrays."""

    ########################################################################

    DEBUG = False

    # True if rows and columns are 1-origin instead of 0-origin
    ONE_ORIGIN = True

    # All alphabetic and digit characters
    POLYBIUS = [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V", "W", "X"],
        ["Y", "Z", "0", "1", "2", "3"],
        ["4", "5", "6", "7", "8", "9"]
    ]

    # a mapping of (row, col) to char, filled by _polybius_reinit()
    _DICT = {}

    # a mapping of char to (row, col), filled by _polybius_reinit()
    _RDICT = {}

    ########################################################################

    def __init__(
        self,
        key=None,
        one_origin=False
    ):
        """Class instance initialization."""
        # set this before calling set_key!
        self.ONE_ORIGIN = one_origin

        if key is None:
            self.set_key(string.uppercase + string.digits)
        else:
            self.set_key(key)

    ########################################################################

    def __str__(self):
        """Return a string representation of the instance."""
        out = []
        out.append("")
        if self.ONE_ORIGIN:
            out.append("  123456")
        else:
            out.append("  012345")
        out.append(" +------")
        for row in range(6):
            s = "".join(self.POLYBIUS[row])
            if self.ONE_ORIGIN:
                out.append("%d|%s" % (row + 1, s))
            else:
                out.append("%d|%s" % (row, s))
        out.append("")
        return "\n".join(out)

    ########################################################################

    def print_polybius(self):
        """Display the contents of POLYBIUS, showing 0-origin."""
        print(self)

    ########################################################################

    def _polybius_dicts(self):
        """Compute forward and reverse dictionaries from POLYBIUS."""
        d = {}
        rd = {}
        for row, rowlist in enumerate(self.POLYBIUS):
            for col, char in enumerate(rowlist):
                if self.ONE_ORIGIN:
                    key = (row + 1, col + 1)
                else:
                    key = (row, col)
                d[key] = char
                rd[char] = key
        return d, rd

    ########################################################################

    def _polybius_reinit(self):
        """Reinitialize after changing the POLYBIUS array."""
        self._DICT, self._RDICT = self._polybius_dicts()

        if self.DEBUG:
            print("_DICT")
            pprint(self._DICT)
            print()

            print("_RDICT")
            pprint(self._RDICT)
            print()

    ########################################################################

    def set_key(self, s, debug=False):
        """Set the elements in POLYBIUS from the characters in s."""
        import string
        # these are the permitted characters
        allowed = string.uppercase + string.digits
        # print("allowed: '%s'" % allowed)

        # others has the permitted characters not yet seen
        others = allowed

        if debug:
            print("Setting the key to '%s'" % s)

        # sort uppercase into key and non-key characters
        seen = set()
        starting_characters = []
        for key in list(s.upper()):
            # check for allowed character first
            if key not in allowed:
                if debug:
                    print("Skipping '%s' because it is not allowed" % key)
                continue
            # then check if it is still in others
            if key not in others:
                if debug:
                    print("Skipping '%s' because it was already seen" % key)
                continue
            # add it to the seen list, starting characters
            seen.add(key)
            starting_characters.append(key)
            # and remove from others
            others = others.replace(key, "")

        # show the resulting partitions
        if debug:
            print("".join(starting_characters))
            print("".join(others))

        new_key = ("".join(starting_characters)) + ("".join(others))
        assert len(new_key) == 36,\
            "Resulting Polybius key has wrong (%d != 36) length?" \
            % len(new_key)

        # transfer the new_key to POLYBIUS
        index = 0
        for row in range(6):
            for col in range(6):
                self.POLYBIUS[row][col] = new_key[index]
                index += 1

        if debug:
            self.print_polybius()

        self._polybius_reinit()

    ########################################################################

    def minval_maxval(self):
        """Return the min and max row/col indices."""
        if self.ONE_ORIGIN:
            minval = 1
        else:
            minval = 0
        return minval, minval + 5

    ########################################################################

    def polybius(self, digit_pairs, alt=None):
        """Return a string corresponding to the digit_pairs."""
        out = []
        # minval, maxval = self.minval_maxval()

        for row, col in digit_pairs:
            # assert(minval <= row <= maxval)
            # assert(minval <= col <= maxval)
            out.append(self.polybius_char(row, col, alt))
            # if self.ONE_ORIGIN:
            #     out.append(self.POLYBIUS[row - 1][col - 1])
            # else:
            #     out.append(self.POLYBIUS[row][col])
        return "".join(out)

    ########################################################################

    def get_key(self):
        """Return the key as a string."""
        return "".join(["".join(s) for s in self.POLYBIUS])

    ########################################################################

    def reset_polybius(self):
        """Reset POLYBIUS to the default string."""
        import string
        # s = string.uppercase + string.digits
        self.set_key(string.uppercase + string.digits)

    ########################################################################

    def upperonly(self, s):
        """Return a string of only valid characters in s.upper()."""
        return "".join([x for x in s.upper() if s.isalnum()])

    ########################################################################

    def polybius_pair(self, c):
        """Convert a character to a (row, col) pair of the Polybius array."""
        return self._RDICT.get(c)

    ########################################################################

    def polybius_char(self, n1, n2, alt=None):
        """Convert a character to a (row, col) pair of the Polybius array."""
        if alt is None:
            return self._DICT.get((n1, n2))
        return self._DICT.get((n1, n2), alt)

    ########################################################################

    def text2pairs(self, t):
        """Convert text string t to Polybius (row, col) pairs."""
        print("text2pairs", "'%s'" % t)
        self.print_polybius()
        out = []
        for c in self.upperonly(t):
            out.append(self._RDICT.get(c))
        return out

    ########################################################################

    def pairs2text(self, pairs_list):
        """Convert (row, col) pairs in pairs_list to a string."""
        out = []
        minval, maxval = self.minval_maxval()
        for r, c in pairs_list:
            # r and c are 0-based
            assert minval <= r <= maxval, "Row error in pairs2text: %s" % r
            assert minval <= c <= maxval, "Column error in pairs2text: %s" % c
            if self.ONE_ORIGIN:
                out.append(self.POLYBIUS[r - 1][c - 1])
            else:
                out.append(self.POLYBIUS[r][c])
        result = "".join(out)
        return result

########################################################################

if __name__ == "__main__":

    ########################################################################

    pb = Polybius6(one_origin=False)
    print(pb)

    pb = Polybius6(one_origin=True)
    print(pb)

    pb = Polybius6("FGHIJK EXYZ0L DW781M CV692N BU543O ATSRQP")
    print(pb)

    pb = Polybius6("FGHIJK EXYZ0L DW781M CV692N BU543O ATSRQP", False)
    print(pb)

    if pb.DEBUG:
        pb.print_polybius()

    pb.reset_polybius()
    pb.print_polybius()

    if pb.ONE_ORIGIN:
        s = pb.polybius([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
    else:
        s = pb.polybius([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    print(s)
    assert(s == "AHOV29"), "Assertion failed: %s" % s

    if pb.ONE_ORIGIN:
        s = pb.polybius([(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)])
    else:
        s = pb.polybius([(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)])
    print(s)
    assert(s == "FKPUZ4"), "Assertion failed: %s" % s

    pb.set_key("09 this is the new key 81", debug=True)
    s = pb.get_key()
    print(s)
    assert s == "09THISENWKY81ABCDFGJLMOPQRUVXZ234567", "get_key error: %s" % s

    if pb.ONE_ORIGIN:
        test = [(x + 1, y + 1) for y in range(6) for x in range(6)]
    else:
        test = [(x, y) for y in range(6) for x in range(6)]
    print(test)
    print(pb.pairs2text(test))
    print()

    CLUE3 = """
44541134541123335344541242434244325141
2123113113531554425442444243443251415343543242
34411125513553341342432253431144543453
43225134314214325134125334121554153451
3351444411225144425442444415345123551543
21345111131121235142543153332142435144531534
1434512542531544335154325341443
435135441
"""

    clues = "".join(CLUE3.split("\n")[1:-1])
    # clues = CLUE3.replace("\n", "")
    if pb.DEBUG:
        print(clues)

    clue_pairs = []
    s = clues
    while s:
        t, s = s[:2], s[2:]
        clue_pairs.append(tuple(map(lambda x: int(x), list(t))))
    if pb.DEBUG:
        print(clue_pairs)

    pb.reset_polybius()
    pb.print_polybius()

    key1 = "AFKPU BGLQV CHMRW DINSX EJOTY".replace(" ", "")
    pb.set_key(key1)
    pb.print_polybius()

    result = pb.polybius(clue_pairs)
    print(result)

    if pb.ONE_ORIGIN:
        key2 = "AFKPUZ BGLQV9 CHMRW8 DINSX7 EJOTY6 012345"
    else:
        key2 = "501234 ZAFKPU 9BGLQV 8CHMRW 7DINSX 6EJOTY"
    pb.set_key(key2)
    pb.print_polybius()
    result = pb.polybius(clue_pairs)
    print(result)
    expected = """
START ALMOST FINISHED BLACKOUT IT IS IN SHED ON THIRD AVE WORKING ON A STRONGER
 CIPHER FOR FUTURE MESSAGES IT IS SURELY UNBREAKABLE IT COMBINES OUR PREVIOUS
 METHODS RWKTD
""".replace("\n", "").replace(" ", "")
    assert result == expected, \
        "Expected: %s\n                     Got: %s" % (expected, result)
