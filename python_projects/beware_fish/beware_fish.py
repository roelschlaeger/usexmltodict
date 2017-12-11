"""Solve location for 'Beware Fish!' cache

http://www.geocaching.com/seek/cache_details.aspx?guid=13eba085-4d71-4004-a839-35b6aa79876c
"""

import simplekml

# output filename
FILENAME = "beware_fish.kml"

# posted cache location
LAT = "N38° 49.025"
LON = "W90° 52.315"


def dmt(v):
    """Convert LAT or LON to (hemisphere, degrees, minutes)"""
    h, v = v[0], v[1:]
    d, v = v[:2], v[2:]
    m = v[1:]
    print(h, d, m)
    return (h, int(d), float(m))


dmt(LAT)
dmt(LON)
print()


def convert(s):
    """Convert N38 49.024 to float result"""
    h, s = s[0], s[1:]
    d, m = map(float, s.split())
    result = d + m / 60.
    if h in ['S', 'W']:
        result = -result
    return result


def undmt(h, d, m):
    s = "%s%02d %2.3f" % (h, d, m)
    return convert(s)


def main():
    kml = simplekml.Kml()
    h0, d0, m0 = dmt(LAT)
    h1, d1, m1 = dmt(LON)
    for x in range(5):
        print(x, end=" ")
        A = x * 20 - 1
        B = x * 6 + 1
        print("%2d" % A, "%2d" % B, end=" ")
        ma = round(m0 + A/1000., 3)
        mb = round(m1 - B/1000., 3)
        print(h0, d0, "%.3f" % ma, end=" ")
        print(h1, d1, "%.3f" % mb, end=" ")
        lat = undmt(h0, d0, ma)
        lon = undmt(h1, d1, mb)
        print(lat, lon)
        name = "Point%s" % x
        coords = [(lon, lat)]
        kml.newpoint(name=name, coords=coords)
    kml.save(FILENAME)
    print("Output is in %s" % FILENAME)



if __name__ == "__main__":
    main()

# end of file
