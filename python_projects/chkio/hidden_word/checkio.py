# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/hidden-word/

from __future__ import print_function

########################################################################


def lines_transpose(s):
    """Transpose the lines in s."""
#   s = s.lower().replace(" ", "")

    # break in to lines
    lines = s.split("\n")

    # count the rows
    rows = len(lines)

    # count the longest line
    cols = max([len(line) for line in lines])

    # create a dictionary for output by column number
    out = {}

    # transpose the characters
    for c in range(cols):

        # start with an empty list
        out.setdefault(c, [])

        # search all rows
        for r in range(rows):

            # bring in one character
            try:
                c2 = lines[r][c]
            except IndexError:
                c2 = " "

            # append the character to the row
            out[c].append(c2)

    # turn the lists back into strings
    result = []
    for c in range(cols):
        result.append("".join(out[c]))

    return result

########################################################################


def checkio(s, key):
    """Find 'key' in the strings in 's', horizontally or vertically."""

    # ensure all lowercase, no white space
    s = s.lower().replace(" ", "")

    # ensure the key is lowercase
    key = key.lower()

    # split string into lines
    lines = s.split("\n")

    # no result from the horizontal search
    result = []

    # look through all lines
    for index, line in enumerate(lines):

        # string search for the key
        loc = line.find(key)

        # if found
        if loc != -1:

            # return the 1-index offsets
            result.extend([index + 1, loc + 1, index + 1, loc + len(key)])
#           print(index, line)

#   print(result)

    # transpose the string
    lines2 = lines_transpose(s)

#   print(lines2)

    # look through all columns
    for index, line in enumerate(lines2):

        # string search for the key
        loc = line.find(key)

        # if found
        if loc != -1:

            # return the 1-index offsets
            result.extend([loc + 1, index + 1, loc + len(key), index + 1])
#           print(index, line)

#   print(result)
    return result

########################################################################

assert checkio(u"""DREAMING of apples on a wall,
And dreaming often, dear,
I dreamed that, if I counted all,
-How many would appear?""", u"ten") == [2, 14, 2, 16]

assert checkio("""He took his vorpal sword in hand:
Long time the manxome foe he sought--
So rested he by the Tumtum tree,
And stood awhile in thought.
And as in uffish thought he stood,
The Jabberwock, with eyes of flame,
Came whiffling through the tulgey wood,
And burbled as it came!""", "noir") == [4, 16, 7, 16]

print("Done!")

# end of file
