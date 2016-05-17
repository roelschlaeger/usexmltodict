# coding=utf-8

"""Perform Polybius encoding."""

from __future__ import print_function

DEBUG = False

POLYBIUS = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "K"],
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"],
]

########################################################################


def print_polybius():
    """Display the contents of POLYBIUS."""
    print()
    for row in range(5):
        s = "".join(POLYBIUS[row])
        print(s)
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
    # allowable characters are "A" - "Z" except "J"
    import string
    others = string.uppercase
    others = others.replace("J", "")

    print("Setting key to %s" % s)
    # sort uppercase into key and non-key characters
    seen = set()
    starting_characters = []
    for key in list(s.upper()):
        if (not key.isalpha()) or key == "J" or key in seen:
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

if DEBUG:

    set_key("this is the new key", debug=True)

########################################################################


def reset_polybius():
    """Reset POLYBIUS to the default string."""
    import string
    # set the key to A-Z except for J
    set_key(string.uppercase.replace("J", ""))

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

if __name__ == "__main__":

    CLUE3 = """
44541134541123335344541242434244325141
2123113113531554425442444243443251415343543242
3441112551355334413424432253431144543453
43225134314214325134125334121554153451
3351444411225144425442444415345123551543
21345111131121235142543153332142435144531534
143451245253154433515432341443
43513544
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

    set_key("SKULL")
    result = polybius(out)
    print(result)
