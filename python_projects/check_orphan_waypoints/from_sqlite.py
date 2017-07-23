# vim:ts=4:sw=4:tw=0:wm=0:et

# =*- encoding=utf-8 -*-

"""

Search sqlite database for orphan geocaches.

SYNOPSIS

    from_sqlite [-h | --help] [-v | --version] [--verbose] [ -k | --kansas ]

DESCRIPTION

    Examine waypoint names in sqlite3.db for orphaned waypoints == no parent
    GC.

EXAMPLES

    from_sqlite

    from_sqlite --kansas

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

from __future__ import print_function

from sqlite3 import connect
from pprint import pprint
import sys

assert sys.version_info >= (3,), "Python3 or better required to run"

__VERSION__ = "0.0.6"  # 20170723 1353 rlo

########################################################################


def get_all_waypoint_names(dbname):
    """Fetch all waypoint names from the SQLite3 database."""
    print("Opening %s" % dbname)

    with connect(dbname) as _connection:

        print("Selecting Code from Caches")
        _selection = _connection.execute('SELECT Code from Caches')

        # get all rows as tuples
        _all = _selection.fetchall()

    # return just the names instead of tuples
    return [x[0] for x in _all]

########################################################################


if __name__ == "__main__":

    import argparse
    import textwrap
    import time

    ########################################################################

    DBNAME = './Default/sqlite.db3'
    KB_DBNAME = './Kansas/sqlite.db3'

    def search_string(result):
        """Return GSAK RE search string.

        Examine the strings in result for likely cache name search strings
        suitable for regular expression searching in GSAK.
        """
        out = []
        for _selection in result:
            if (_selection[0].isdigit()) and (len(_selection) == 5):
                out.append(_selection)

        return "|".join(out)

    def main():
        """Compute all waypoint names that don't have a geocache parent."""
        dbname = DBNAME
        if OPTIONS.kansas:
            dbname = KB_DBNAME

        print("Processing from %s" % dbname)

        print()

        _all = get_all_waypoint_names(dbname)

        # get all non-geocache names
        non = [x for x in _all if x[:2] != 'GC']
        print(len(non), "non-cache waypoints")

        # get all geocache names
        _gc_waypoints = [x for x in _all if x[:2] == 'GC']
        print(len(_gc_waypoints), "cache waypoints")

        print()

        # locate non-cache waypoints without cache parents
        result = {}
        for _non_cache_wpt in non:

            # skip names that are too short
            if len(_non_cache_wpt) <= 2:
                continue

            # the 'trait' is formed by skipping the first two characters of a
            # name
            trait = _non_cache_wpt[2:]
            if 2 <= len(trait) <= 5:
                gcname = "GC" + trait
                if gcname not in _gc_waypoints:
                    if trait not in result:
                        result[trait] = []
                    result[trait].append(_non_cache_wpt)

        print(len(result), "waypoints without a parent")
        print()
        pprint(result)

        print()
        print("Regular expression search string:")
        print(search_string(result))

        return 0

    ########################################################################

    try:

        START_TIME = time.time()

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

        PARSER.add_argument(
            '-k',
            '--kansas',
            action='store_true',
            default=False,
            help='use Kansas database'
        )

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - START_TIME) / 60.0)

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
