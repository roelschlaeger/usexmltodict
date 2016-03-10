#! C:\Users\Robert Oelschlaeger\AppData\Local\Programs\Python\Python35\python35.EXE

# if run from python2.x, support print()
from __future__ import print_function

__VERSION__ = "0.0.3"

from sqlite3 import connect
from pprint import pprint

########################################################################


def get_all_waypoint_names(dbname):
    """Fetch all waypoint names from the SQLite3 database"""

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

    ########################################################################

    DBNAME = './Default/sqlite.db3'

    def main():

        """Compute all waypoint names that don't have a geocache parent"""

        print()

        all = get_all_waypoint_names(DBNAME)

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
                if not gcname in gc:
                    if trait not in result:
                        result[trait] = []
                    result[trait].append(n)

        print(len(result), "waypoints without a parent")
        print()
        pprint(result)

    ########################################################################

    main()

# end of file
