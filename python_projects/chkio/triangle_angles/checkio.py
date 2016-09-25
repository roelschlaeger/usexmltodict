# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/triangle-angles/

### The law of cosines
### cos(A)=frac{b^2+c^2-a^2}{2*b*c}
###
### cos(B)=frac{a^2+c^2-b^2}{2*a*c}
###
### cos(C)=frac{a^2+b^2-c^2}{2*a*b}

from math import acos, degrees


def dacos(x):
    """Return the angle in degrees whose cosine is x."""
    return degrees(acos(x))


def checkio(a, b, c):
    """Compute the sorted angles of an arbitrary triangle."""

    # check for impossible triangle
    a, b, c = sorted([a, b, c])
    if (a + b) <= c:
        # fabricate phony result
        aa, bb, cc = [0, 0, 0]
    else:

        # compute cosines from the law of cosines
        cosA = (b ** 2 + c ** 2 - a ** 2) / (2. * b * c)
        cosB = (a ** 2 + c ** 2 - b ** 2) / (2. * a * c)
        cosC = (a ** 2 + b ** 2 - c ** 2) / (2. * a * b)

        # compute the angles
        a = round(dacos(cosA), 0)
        b = round(dacos(cosB), 0)
        c = round(dacos(cosC), 0)

        # sort and convert to integers
        aa, bb, cc = map(int, sorted([a, b, c]))

#   print([aa, bb, cc])

    # return sorted result
    return [aa, bb, cc]

checkio(3, 4, 5)
checkio(4, 4, 4)
checkio(2, 2, 5)
checkio(10, 20, 29.9)


# end of file
