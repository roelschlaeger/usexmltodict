# vim:ts=4:sw=4:tw=0:wm=0:et:noic


def build_paths(data):
    """Build list of (start, end, waypoints) tuples for a route."""
    # lats, lons, texts, syms, names = list(zip(*data)][4]
    names = list(zip(*data))[4]

    waypoints = []

    # tuples of (start, end, waypoints[])
    results = []

    for index, name in enumerate(names):
        if (index == 0):
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


if __name__ == "__main__":

    from with_sqlite3 import get_data

    data = get_data()

    results = build_paths(data)

    for start, end, waypoints in results:
        print()
        print("From: %s" % str(data[start]))
        if waypoints:
            for waypoint in waypoints:
                print("    : %s" % str(data[waypoint]))
        print("  To: %s" % str(data[end]))

# end of file
