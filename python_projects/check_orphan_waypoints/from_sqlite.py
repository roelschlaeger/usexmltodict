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

__VERSION__ = "0.0.5"

########################################################################


def get_all_waypoint_names(dbname):
    """Fetch all waypoint names from the SQLite3 database."""
    print("Opening %s" % dbname)

    with connect(dbname) as c:

        print("Selecting Code from Caches")
        c2 = c.execute('SELECT Code from Caches')

        # get all rows as tuples
        all = c2.fetchall()

    # return just the names instead of tuples
    return [x[0] for x in all]

########################################################################


if __name__ == "__main__":

    import argparse
    import os
    import sys
    import textwrap
    import time
    import traceback

    ########################################################################

    DBNAME = './Default/sqlite.db3'
    KB_DBNAME = './Kansas/sqlite.db3'

    def search_string(result):
        """Return GSAK RE search string.

        Examine the strings in result for likely cache name search strings
        suitable for regular expression searching in GSAK.
        """
        out = []
        for s in result:
            if (s[0].isdigit()) and (len(s) == 5):
                out.append(s)

        return "|".join(out)

    def main():
        """Compute all waypoint names that don't have a geocache parent."""
        dbname = DBNAME
        if OPTIONS.kansas:
            dbname = KB_DBNAME

        print("Processing from %s" % dbname)

        print()

        all = get_all_waypoint_names(dbname)

        # get all non-geocache names
        non = [x for x in all if x[:2] != 'GC']
        print(len(non), "non-cache waypoints")

        # get all geocache names
        gc = [x for x in all if x[:2] == 'GC']
        print(len(gc), "cache waypoints")

        print()

        # locate non-cache waypoints without cache parents
        result = {}
        for n in non:

            # skip names that are too short
            if len(n) <= 2:
                continue

            # the 'trait' is formed by skipping the first two characters of a
            # name
            trait = n[2:]
            if 2 <= len(trait) <= 5:
                gcname = "GC" + trait
                if gcname not in gc:
                    if trait not in result:
                        result[trait] = []
                    result[trait].append(n)

        print(len(result), "waypoints without a parent")
        print()
        pprint(result)

        print()
        print("Regular expression search string:")
        print(search_string(result))

    ########################################################################

    try:

        START_TIME = time.time()

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

    except KeyboardInterrupt, error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit, error_exception:               # sys.exit()
        raise error_exception

    except Exception, error_exception:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(error_exception))
        traceback.print_exc()
        os._exit(1)

# end of file
