# coding=utf-8

"""Perform Polybius encoding."""

from __future__ import print_function
from pprint import pprint

########################################################################

DEBUG = False

# "Z" is not permitted in the POLYBIUS array
POLYBIUS = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "J"],
    ["K", "L", "M", "N", "O"],
    ["P", "Q", "R", "S", "T"],
    ["U", "V", "W", "X", "Y"],
]

# a mapping of (row, col) to char, filled by _polybius_reinit()
_DICT = {}

# a mapping of char to (row, col), filled by _polybius_reinit()
_RDICT = {}

########################################################################


def _polybius_dicts():
    """Compute forward and reverse dictionaries from POLYBIUS."""
    d = {}
    rd = {}
    for row, rowlist in enumerate(POLYBIUS):
        for col, char in enumerate(rowlist):
            # row and column are offset by 1!
            key = (row + 1, col + 1)
            d[key] = char
            rd[char] = key
    return d, rd

########################################################################


def _polybius_reinit():
    """Reinitialize after changing the POLYBIUS array."""
    global _DICT
    global _RDICT

    _DICT, _RDICT = _polybius_dicts()

    print("_DICT")
    pprint(_DICT)
    print()

    print("_RDICT")
    pprint(_RDICT)
    print()

########################################################################


def print_polybius():
    """Display the contents of POLYBIUS, showing 1-origin."""
    print()
    print("  12345")
    print(" +-----")
    for row in range(5):
        s = "".join(POLYBIUS[row])
        print("%d|%s" % (row + 1, s))
    print()

if DEBUG:
    print_polybius()

########################################################################


def polybius(digit_pairs):
    """Return a string corresponding to the digit_pairs."""
    out = []
    for row, col in digit_pairs:
        assert(row < 5)
        assert(col < 5)
        out.append(POLYBIUS[row][col])
    return "".join(out)

########################################################################


def set_key(s, debug=False):
    """Set the elements in POLYBIUS from the characters in s."""
    # allowable characters are "A" - "Y"
    import string
    others = string.uppercase
    others = others.replace("Z", "")

    print("Setting key to %s" % s)
    # sort uppercase into key and non-key characters
    seen = set()
    starting_characters = []
    for key in list(s.upper()):
        assert key != "Z", "'Z' is not allowed in the Polybius key"
        if (not key.isalpha()) or key == "Z" or key in seen:
            continue
        seen.add(key)
        starting_characters.append(key)
        others = others.replace(key, "")

    # show the resulting partitions
    if debug:
        print("".join(starting_characters))
        print("".join(others))

    global POLYBIUS
    new_key = ("".join(starting_characters)) + ("".join(others))
    assert len(new_key) == 25,\
        "Resulting Polybius key has wrong (%d != 25) length?" % len(new_key)

    # transfer the new_key to POLYBIUS
    index = 0
    for row in range(5):
        for col in range(5):
            POLYBIUS[row][col] = new_key[index]
            index += 1

    if debug:
        print_polybius()

    _polybius_reinit()

if DEBUG:

    set_key("this is the new key", debug=True)

########################################################################


def reset_polybius():
    """Reset POLYBIUS to the default string."""
    import string
    # set the key to A-Y; no Z
    set_key(string.uppercase.replace("Z", ""))

########################################################################

if DEBUG:
    reset_polybius()

    s = polybius([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), ])
    print(s)
    assert(s == "AGNTZ")

    s = polybius([(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)])
    print(s)
    assert(s == "EINRV")

########################################################################


def upperonly(s):
    """Return a string of only alphanumeric characters in s.upper()."""
    return "".join([x for x in s.upper() if s.isalpha()])

########################################################################


def text2pairs(t):
    """Convert text string t to Polybius (row, col) pairs."""
    print("text2pairs", "'%s'" % t)
    print_polybius()
    out = []
    for c in upperonly(t):
        out.append(_RDICT.get(c, (-1, -1)))
    return out

########################################################################


def pairs2text(pairs_list):
    """Convert (row, col) pairs in pairs_list to a string."""
    out = []
    for r, c in pairs_list:
        # r and c are 1-based
        assert 1 <= r <= 5, "Row error in pairs2text: %s" % r
        assert 1 <= c <= 5, "Column error in pairs2text: %s" % c
        out.append(POLYBIUS[r - 1][c - 1])
    result = "".join(out)
    return result


########################################################################

if __name__ == "__main__":

    test = [(x, y) for y in range(1, 6) for x in range(1, 6)]
    print(test)
    print(pairs2text(test))
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
    if DEBUG:
        print(clues)

    out = []
    s = clues
    while s:
        t, s = s[:2], s[2:]
        out.append(tuple(map(lambda x: int(x) - 1, list(t))))
    if DEBUG:
        print(out)

    reset_polybius()
    print_polybius()

    key1 = "AFKPU BGLQV CHMRW DINSX EJOTY".replace(" ", "")
    set_key(key1)
    print_polybius()

    result = polybius(out)
    print(result)
