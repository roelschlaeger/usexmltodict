# vim:ts=4:sw=4:tw=0:wm=0:et
# =*- encoding=utf-8 -*-

"""Locate found files beginning with each letter of the alphabet."""

# if run from python2.x, support print()
from __future__ import print_function

from sqlite3 import connect
import sys
assert sys.version_info > (3, ), "Python 3 required"

__VERSION__ = "0.0.2"  # 20170723 1405 rlo

########################################################################

DBNAME = './My Finds/sqlite.db3'

########################################################################


def get_all_waypoints(dbname):
    """Fetch all waypoint names from the SQLite3 database."""
    print("Opening %s" % dbname)

    with connect(dbname) as _connection:

        print("Selecting Code from Caches")
        _selection = _connection.execute(
            'SELECT Code, Name, PlacedBy, FoundByMeDate \
            FROM Caches ORDER BY FoundByMeDate DESC'
        )

        # get all rows as tuples
        _all_names = _selection.fetchall()

    # return just the names instead of tuples
    return _all_names

########################################################################


def calculate_widths(_data):
    """Calculate the widths of the output fields."""
    w_1 = w_2 = w_3 = w_4 = 0

    for _key, values in _data.items():
        w_1 = max(w_1, len(values[0]))
        w_2 = max(w_2, len(values[1]))
        w_3 = max(w_3, len(values[2]))
        w_4 = max(w_4, len(values[3]))

    # print(w_1, w_2, w_3, w_4)
    return w_1, w_2, w_3, w_4

########################################################################


def print_results(out):
    """Print the contents of the computed results."""
    w_1, w_2, w_3, w_4 = calculate_widths(out)
    _format = "%%c:  %%-%ds  %%-%ds  %%-%ds  %%-%ds" % (w_1, w_2, w_3, w_4)
    print()
    print(_format % ("A", "GC", "Name", "Owner", "Found Date"))
    print(_format % ("-", "-" * w_1, "-" * w_2, "-" * w_3, "-" * w_4))
    for key in sorted(out):
        value = out[key]
        print(_format % (key, value[0], value[1], value[2], value[3]))
    print()

########################################################################


def main():
    """Compute alphabet challenge."""
    dbname = DBNAME

    print("Processing from %s" % dbname)
    print()

    _all_names = get_all_waypoints(dbname)

    # get all geocache names
    _gc_name = [x for x in _all_names if x[0][:2] == 'GC']
    # print(len(_gc_name), "cache waypoints")

    out = {}
    import string
    for _char in string.ascii_uppercase:  # + string.digits + string.lowercase:
        # print(_char)
        for item in _gc_name:
            if item[1][0] == _char:
                # print(item[1])
                out[_char] = item
                # print("%c: %s" % (_char, out[_connection][1]))
                break
    print_results(out)

    return 0


########################################################################

if __name__ == '__main__':

    # import sys
    import argparse
    import textwrap
    # import traceback
    # import os

    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=textwrap.dedent(globals()['__doc__']),
        # version="Version: %s" % __VERSION__
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

    # except Exception as error_exception:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(error_exception))
    #     traceback.print_exc()
    #     os._exit(1)

# end of file
