# vim:ts=4:sw=4:tw=0:wm=0:et
# =*- encoding=utf-8 -*-

"""Locate found files with specific baseball terms."""

# if run from python2.x, support print()
from __future__ import print_function
from sqlite3 import connect
from collections import defaultdict

import sys
assert sys.version_info > (3, ), "Python 3 required"

__VERSION__ = "0.0.3"  # 20170723 1422 rlo: Update for Python3

########################################################################

DBNAME = './My Finds/sqlite.db3'

KEYWORDS = [
    "BASEBALL",
    "FIRST",
    "SECOND",
    "THIRD",
    "HOME",
    "BALL",
    "STRIKE",
    "WALK",
    "SINGLE",
    "DOUBLE",
    "TRIPLE",
    "HOMERUN",
    "INNING",
    "PLAYER",
    "MANAGER",
    "COACH",
    "FIELD",
    "CARDINALS",
    "CUBS",
    "PIRATES",
    "REDS",
    "PHILLIES",
    "BREWERS",
]

# Added this list of team names 20170723 rlo
TEAMS = [
    "ANGELS",
    "ASTROS",
    "ATHLETICS",
    "BLUE JAYS",
    "BRAVES",
    "BREWERS",
    "CARDINALS",
    "CUBS",
    "DIAMONDBACKS",
    "DODGERS",
    "GIANTS",
    "INDIANS",
    "MARINERS",
    "MARLINS",
    "METS",
    "NATIONALS",
    "ORIOLES",
    "PADRES",
    "PHILLIES",
    "PIRATES",
    "RANGERS",
    "RAYS",
    "REDS",
    "REDSOX",
    "ROCKIES",
    "ROYALS",
    "TIGERS",
    "TWINS",
    "WHITE SOX",
    "YANKEES"
]

# KEYWORDS += TEAMS

########################################################################


def build_query(keywords):
    """Create a query from the keywords."""
    _c1 = "SELECT Code, Name, PlacedBy, FoundByMeDate FROM Caches"
    _c3 = "ORDER BY FoundByMeDate DESC"

    clist = []
    for _w in keywords:
        clist.append('UPPER(Name) LIKE "%%_%s_%%"' % _w.upper())
    _c2 = "WHERE " + " or ".join(clist)

    return "%s %s %s" % (_c1, _c2, _c3)

########################################################################


def get_all_waypoints(dbname):
    """Fetch all waypoint names from the SQLite3 database."""
    print("Opening %s" % dbname)

    with connect(dbname) as _connection:

        print("Selecting Code from Caches")

        query = build_query(KEYWORDS)
        # query = build_query(TEAMS)
        print(query)

        _query_result = _connection.execute(query)
        #   'SELECT Code, Name, PlacedBy, FoundByMeDate
        #   FROM Caches ORDER BY FoundByMeDate DESC'
        # )

        # get all rows as tuples
        _all_names = _query_result.fetchall()

    # return just the names instead of tuples
    return _all_names

########################################################################


def calculate_widths(_data):
    """Calculate the widths of the output fields."""
    w_0 = w_1 = w_2 = w_3 = w_4 = 0

    for key, valuelist in _data.items():
        w_0 = max(w_0, len(key))
        for values in valuelist:
            w_1 = max(w_1, len(values[0]))
            w_2 = max(w_2, len(values[1]))
            w_3 = max(w_3, len(values[2]))
            w_4 = max(w_4, len(values[3]))

    # print(w0, w1, w2, w3, w4)
    return w_0, w_1, w_2, w_3, w_4

########################################################################


def print_results(out):
    """Print the contents of the computed results."""
    w_0, w_1, w_2, w_3, w_4 = calculate_widths(out)
    _format = "%%-%ds:  %%-%ds  %%-%ds  %%-%ds  %%-%ds" % (
        w_0, w_1, w_2, w_3, w_4
        )
    print()
    print(_format % ("String", "GC", "Name", "Owner", "Found Date"))
    print(_format % ("-" * w_0, "-" * w_1, "-" * w_2, "-" * w_3, "-" * w_4))
    for key in KEYWORDS:
        if key not in out:
            continue
        for value in out[key]:
            print(_format % (key, value[0], value[1], value[2], value[3]))
    print()

########################################################################


def compute_baseball_challenge():
    """Compute baseball challenge."""
    dbname = DBNAME

    print("Processing from %s" % dbname)
    print()

    _all_names = get_all_waypoints(dbname)

    # get all geocache names
    _gc = [x for x in _all_names if x[0][:2] == 'GC']
    # print(len(_gc), "cache waypoints")

    out = defaultdict(list)
    for _keyword in KEYWORDS:
        print(_keyword)
        for item in _gc:
            if item[1].upper().find(_keyword) >= 0:
                # print(item[1])
                out[_keyword].append(item)
                # print("%_keyword: %s" % (_keyword, out[_keyword][1]))
#               break
        # else:
        # if len(out[_keyword]) == 0:
        if not out[_keyword]:
            print("Nothing found for %s" % _keyword)
    print_results(out)

########################################################################


def main():
    """main routine called from command line."""
    compute_baseball_challenge()
    return 0


########################################################################

if __name__ == '__main__':

    import argparse
    import textwrap

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
