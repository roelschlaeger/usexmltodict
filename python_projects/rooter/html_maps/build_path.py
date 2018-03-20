#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:noic

"""Create a list of (start, end, waypoint) tuples for a route."""

########################################################################


def build_paths(data, single_route_flag=False):
    """Build list of (start, end, waypoints) tuples for a route."""
    # lats, lons, texts, syms, names = list(zip(*data)][4]
    names = list(zip(*data))[4]

    waypoints = []

    # tuples of (start, end, waypoints[])
    results = []

    if single_route_flag:
        start = 0
        end = len(names) - 1
        results.append((start, end, list(range(1, end))))
    else:
        for index, name in enumerate(names):
            if index == 0:
                waypoints = []
                start = index
            elif name.startswith("GC"):
                end = index
                results.append((start, end, waypoints))
                start = index
                waypoints = []
            elif not name.startswith("GC"):
                waypoints.append(index)

        # go from last location back to first
        end = 0
        results.append((start, end, waypoints))

    return results


########################################################################


if __name__ == "__main__":

    from with_sqlite3 import get_data

    DATA = get_data()

    RESULTS = build_paths(DATA, True)

    for START, END, WAYPOINTS in RESULTS:
        print()
        print("From: %s" % str(DATA[START]))
        if WAYPOINTS:
            for WAYPOINT in WAYPOINTS:
                print("    : %s" % str(DATA[WAYPOINT]))
        print("  To: %s" % str(DATA[END]))

# end of file
