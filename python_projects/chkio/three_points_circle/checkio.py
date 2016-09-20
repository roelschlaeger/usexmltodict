# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/three-points-circle/

# http://mathforum.org/library/drmath/view/55239.html

#        |x1^2+y1^2  y1  1|        |x1  x1^2+y1^2  1|
#        |x2^2+y2^2  y2  1|        |x2  x2^2+y2^2  1|
#        |x3^2+y3^2  y3  1|        |x3  x3^2+y3^2  1|
#    h = ------------------,   k = ------------------
#            |x1  y1  1|               |x1  y1  1|
#          2*|x2  y2  1|             2*|x2  y2  1|
#            |x3  y3  1|               |x3  y3  1|

#    r = sqrt((x1-h)^2 + (y1-k)^2)

import re
from math import sqrt

def det3(z):
    """Return the determinant of z."""
    a, b, c = z[0:3]
    d, e, f = z[3:6]
    g, h, i = z[6:9]

    return (
        float(a * float(e * i - f * h)) -
        float(d * float(b * i - c * h)) +
        float(g * float(b * f - c * e))
    )


def checkio(s):
    """Compute the equation of the circle given input points in a string."""

    coordinates = re.match(
        "\((\d+),(\d+)\),\((\d+),(\d+)\),\((\d+),(\d+)\)", s
    )
    vertices = map(int, coordinates.groups())

    x1, y1, x2, y2, x3, y3 = vertices
    n1 = [
        x1 ** 2 + y1 ** 2, y1, 1,
        x2 ** 2 + y2 ** 2, y2, 1,
        x3 ** 2 + y3 ** 2, y3, 1
    ]

    d1 = [
        x1, y1, 1,
        x2, y2, 1,
        x3, y3, 1
    ]

    x = det3(n1) / (2 * det3(d1))

    n2 = [
        x1, x1 ** 2 + y1 ** 2, 1,
        x2, x2 ** 2 + y2 ** 2, 1,
        x3, x3 ** 2 + y3 ** 2, 1,
    ]

    y = det3(n2) / (2 * det3(d1))

    r = sqrt((x - x1) ** 2 + (y - y1) ** 2)

    def round2(f):
        return round(f, 2)

    result = "(x-%g)^2+(y-%g)^2=%g^2" % tuple(map(round2, (x, y, r)))
    return result


assert checkio("(2,2),(6,2),(2,6)") == "(x-4)^2+(y-4)^2=2.83^2"
assert checkio("(3,7),(6,9),(9,7)") == "(x-6)^2+(y-5.75)^2=3.25^2"

print("Done!")
