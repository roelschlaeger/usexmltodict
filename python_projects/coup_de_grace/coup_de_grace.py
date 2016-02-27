from __future__ import print_function

TRANSLATE_PAIRS = {
    'B': '1',
    'Z': '0',
    'X': '2',
    'D': '3',
    'V': '4',
    'F': '5',
    'T': '6',
    'H': '7',
    'R': '8',
    'J': '9',
}

KEYS = "".join(list(TRANSLATE_PAIRS.keys()))
VALUES = "".join(list(TRANSLATE_PAIRS.values()))

import sys
if sys.version_info < (3,):
    import string
    TABLE = string.maketrans(KEYS, VALUES)
else:
    TABLE = str.maketrans(KEYS, VALUES)


def coup_de_grace(s):

    s = s.upper()
    s = s.replace("\n", "")
    print(s)

    result = s.translate(TABLE)
    print(result)

    latmin = result[0:2]
    latminthou = result[2:5]
    lonmin = result[5:7]
    lonminthou = result[7:10]

    latitude = "N38 %2s.%3s" % (latmin, latminthou)
    longitude = "W90 %2s.%3s" % (lonmin, lonminthou)

    return (latitude, longitude)


latitude, longitude = coup_de_grace("XXDDD\nXDRRR")

print(latitude, longitude)
