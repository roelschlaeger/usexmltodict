# vim:ts=4:sw=4:tw=0:wm=0:et
# =*- encoding=utf-8 -*-

"""Locate found files beginning with each letter of the alphabet."""

# if run from python2.x, support print()
from __future__ import print_function

from sqlite3 import connect

__VERSION__ = "0.0.1"

########################################################################

DBNAME = './My Finds/sqlite.db3'

########################################################################


def get_all_waypoints(dbname):
    """Fetch all waypoint names from the SQLite3 database."""
    print("Opening %s" % dbname)

    with connect(dbname) as c:

        print("Selecting Code from Caches")
        c2 = c.execute(
            'SELECT Code, Name, PlacedBy, FoundByMeDate \
            FROM Caches ORDER BY FoundByMeDate DESC'
        )

        # get all rows as tuples
        all = c2.fetchall()

    # return just the names instead of tuples
    return all

########################################################################


def calculate_widths(d):
    """Calculate the widths of the output fields."""
    w1 = w2 = w3 = w4 = 0

    for key, values in d.items():
        w1 = max(w1, len(values[0]))
        w2 = max(w2, len(values[1]))
        w3 = max(w3, len(values[2]))
        w4 = max(w4, len(values[3]))

    # print(w1, w2, w3, w4)
    return w1, w2, w3, w4

########################################################################


def print_results(out):
    """Print the contents of the computed results."""
    w1, w2, w3, w4 = calculate_widths(out)
    format = "%%c:  %%-%ds  %%-%ds  %%-%ds  %%-%ds" % (w1, w2, w3, w4)
    print()
    print(format % ("A", "GC", "Name", "Owner", "Found Date"))
    print(format % ("-", "-" * w1, "-" * w2, "-" * w3, "-" * w4))
    for key in sorted(out):
        value = out[key]
        print(format % (key, value[0], value[1], value[2], value[3]))
    print()

########################################################################


def main():
    """Compute alphabet challenge."""
    dbname = DBNAME

    print("Processing from %s" % dbname)
    print()

    all = get_all_waypoints(dbname)

    # get all geocache names
    gc = [x for x in all if x[0][:2] == 'GC']
    # print(len(gc), "cache waypoints")

    out = {}
    import string
    for c in string.uppercase:  # + string.digits + string.lowercase:
        # print(c)
        for item in gc:
            if item[1][0] == c:
                # print(item[1])
                out[c] = item
                # print("%c: %s" % (c, out[c][1]))
                break
    print_results(out)

########################################################################

if __name__ == '__main__':

    import sys
    import argparse
    import textwrap
    import traceback
    import os

    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=textwrap.dedent(globals()['__doc__']),
        version="Version: %s" % __VERSION__
    )

    PARSER.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help='verbose output'
    )

    OPTIONS = PARSER.parse_args()

    try:
        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit as error_exception:               # sys.exit()
        raise error_exception

    except Exception as error_exception:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(error_exception))
        traceback.print_exc()
        os._exit(1)

# end of file
