"""final locations for Vitt's Mill geocache.

GC6XTEP
Union History - Vitt's Mill
http://www.geocaching.com/seek/cache_details.aspx?guid=445d86d0-97ee-48c3-8d06-728280b1cd82

Short bush wack to the final. Might pick up some beggar's lice along the way!
There is good parking on the West side of the cache.
"""

from __future__ import print_function
from geopy.distance import vincenty
from simplekml import Kml
import re

A = 6   # known answers
B = 5
C = 7

D = 0   # unknown answers
E = 0
F = 0

HOME = (38.45625, -91.002933)  # posted coordinates
WP2 = (38.446733, -91.00035)  # WP2 coordinates
FILENAME = "vittsmill.kml"


def convert(s):
    """Convert latitude or longitude string to degrees."""
    m = re.match("(.)(\d+) (\d+).(\d+)", s)
    c, d, m, t = m.groups()
    d, m, t = map(int, [d, m, t])
    m += t / 1000.
    d += m / 60.
    if c in "SW":
        d = -d
    return d


def main():
    """Compute longitude to fit with computed latitude and checksum."""
    kml = Kml()

    kml.newpoint(name="Vitts Mill", coords=[(HOME[1], HOME[0])])
    kml.newpoint(name="Vitts Mill WP2", coords=[(WP2[1], WP2[0])])

    # known values for A, B, C
    lat = "N38 27.%d%d%d" % (A, B, C)
    clat = convert(lat)

    # all answers sum to 24
    leftovers = 24 - (A + B + C)

    # compute all values for D, E and F
    for D in range(10):
        if D > leftovers:
            continue
        for E in range(10):
            if (D + E) > leftovers:
                continue
            for F in range(10):
                if D + E + F == leftovers:
                    lon = "W91 00.%d%d%d" % (D, E, F)
                    clon = convert(lon)
                    here = (clat, clon)
                    # compute distance from posted coordinates
                    d = vincenty(HOME, here).miles
                    print(d, lat, lon)
                    name = "loc_%d%d%d%d%d%d" % (A, B, C, D, E, F)
                    kml.newpoint(name=name, coords=[(clon, clat)])
    kml.save(FILENAME)
    print("Output is in %s" % FILENAME)

main()

# end of file
