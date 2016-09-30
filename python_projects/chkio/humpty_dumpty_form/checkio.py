# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/humpty-dumpty/

from math import pi, sqrt
from math import asin as arcsin
from math import log as ln


def checkio(h, w):
    # equatorial radius = a
    a = w / 2.0

    # polar radius = c
    c = h / 2.0

    volume = (4.0 / 3.0) * pi * a ** 2 * c

    if (c > a):
        # prolate spheroid: polar radius > equatorial radius
        # http://mathworld.wolfram.com/ProlateSpheroid.html

        # ellipticity = e
        e = sqrt(1.0 - (a ** 2) / (c ** 2))

        area = 2.0 * pi * a ** 2 + 2.0 * pi * a * c / e * arcsin(e)

    elif (c < a):
        # oblate spheroid: polar radius < equatorial radius
        # http://mathworld.wolfram.com/OblateSpheroid.html

        # ellipticity = e
        e = sqrt(1.0 - (c ** 2) / (a ** 2))

        area = (2.0 * pi * a ** 2) + (pi * c ** 2 / e) * ln((1 + e) / (1 - e))

    else:
        # sphere: 4 pi r^2
        area = 4.0 * pi * a ** 2

    print(volume, area)
    return map(lambda x: round(x, 2), [volume, area])

assert checkio(4, 2) == [8.38, 21.48]
assert checkio(2, 2) == [4.19, 12.57]
assert checkio(2, 4) == [16.76, 34.69]

# end of file
