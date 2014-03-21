#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 20 Mar 2014 05:37:46 PM CDT
# Last Modified: Fri 21 Mar 2014 01:32:44 PM CDT

"""
SYNOPSIS

    TODO 3rail [-h] [-v,--verbose] [--version]

DESCRIPTION

    Solve a Three Rail cipher
    http://www.geocaching.com/geocache/GC3ENVJ_3-rail-fence?guid=b8d2806c-f795-4a21-a4e3-718045938144

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "0.0.1"

########################################################################

TEXT = """WYEAOARHSNEENUNVSRIIOIOHTOSECN FUDTOTTREEEFVFVPITORIEIEETOTSX ONFUSXYNAUKBNNHEVIIOFNFWFYPTRTE"""

TEXT = TEXT.replace(" ", "")

print len(TEXT), TEXT

MODULUS = 4


def adjustlength(n):

    text = TEXT

    # adjust length
    l = len(TEXT) % n
    if l:
        text += "." * (n-l)

    return text

def transpose(n):
    print "%2d" % n, "#" * 69

    text = adjustlength(n)

    while text:
        part, text = text[:n], text[n:]
        print part
    print 72 * '#'

def railfence():

#   text = list(adjustlength(4))

    text = list(TEXT)
    l = len(text)

    out = ["?"] * l

    for i in range(0, l, 4):
        out[i] = text.pop(0)
    for i in range(1, l, 2):
        out[i] = text.pop(0)
    for i in range(2, l, 4):
        out[i] = text.pop(0)

    print "".join(out)

def main():

    if 0:
        text = TEXT
        l = len(text) % MODULUS
        if l:
            text += "." * (MODULUS - l)

        a = []
        b = []
        c = []
        while text:

            others, text = text[:MODULUS], text[MODULUS:]

            w, x, y, z = others[:]

            a.extend([w])
            b.extend([x,z])
            c.extend([y])

        print "".join(a)
        print "".join(b)
        print "".join(c)

    elif 0:

        for l in range(2,26):
            transpose(l)

    else:

        railfence()

main()

    ########################################################################
