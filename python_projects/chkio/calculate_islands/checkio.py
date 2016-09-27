# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/calculate-islands/

########################################################################

# eight directions around the current (row, col)
DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

########################################################################


def search_island(islands, r, c, island_marker):
    """Investigate the land mass in 'islands' around (r, c), marking each bit
with 'island_marker'."""

    # repeated calculation of map dimensions
    rows = len(islands)
    cols = len(islands[0])

    # mark the starting spot as visited
    islands[r][c] = island_marker

    # count the starting spot as having been counted
    area = 1

    # push it to the processing stack
    stack = [(r, c)]

    while stack:

        # get the known spot of land
        r0, c0 = stack.pop()

        # look for adjacent spots
        for roff, coff in DIRECTIONS:

            # compute new adjacent location
            r1 = r0 + roff
            c1 = c0 + coff

            # verify it is within map boundaries
            if (r1 < 0) or (r1 >= rows):
                continue
            if (c1 < 0) or (c1 >= cols):
                continue

            # check for non-visited spot of land
            if islands[r1][c1] == 1:

                # push the spot to be visited
                stack.append((r1, c1))

                # mark it as seen
                islands[r1][c1] = island_marker

                # count the spot as having been counted
                area += 1

    # return modified islands map and area count
    return islands, area

########################################################################


def checkio(islands):
    """Compute area of island land masses."""

    rows = len(islands)
    cols = len(islands[0])

    areas = []

    island_marker = 1  # marker for found island, beginning with 2

    # check all rows
    for r in range(rows):

        # check all columns
        for c in range(cols):

            # has this spot been visited?
            if islands[r][c] == 1:

                island_marker += 1
                islands, area = search_island(islands, r, c, island_marker)

                # save the area
                areas.append(area)

    return sorted(areas)

########################################################################

checkio([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]]) == [1, 3]

checkio([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0]]) == [5]

checkio([
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]]) == [2, 3, 3, 4]

print("Done!")

# end of file
