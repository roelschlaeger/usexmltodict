#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 29 Sep 2016 05:04:22 PM CDT
# Last Modified: Thu 29 Sep 2016 06:01:25 PM CDT

"""Find the path from 'start' to 'end' that is less costly than the 'direct'
path."""

from __future__ import print_function

from pprint import pprint
from sys import exit

########################################################################


def compute_path_string(steps, path_list):
    out = []
    a = path_list.pop(0)
    while path_list:
        b = path_list.pop(0)
        c = (steps[(a, b)])
        out.append(c)
        a = b
    result = "".join(out)
    print("compute_path_string", result)
    return result

########################################################################


def direct_path(direct, start, steps):
    # each step cost 2 units
    direct_cost = len(direct) * 2

    # the path is the start location and the reversed direct path computed
    # by astar
    direct_list = [start]
    direct_list.extend([x for x in direct[::-1]])
    direct_string = compute_path_string(steps, direct_list)

    # the returned path is (cost, list_of_nodes, directions)
    path = (
        direct_cost,
        direct_list,
        direct_string
    )

    return path

########################################################################


def find_path(steps, direct, start, end, from_start, b_to_b, to_end):
    """Find the path from 'start' to 'end' that is less costly than the
'direct' path."""

    if 0:
        print("direct")
        pprint(direct, width=40)

        print("start")
        pprint(start, width=40)

        print("end")
        pprint(end, width=40)

        print("from_start")
        pprint(from_start, width=40)

        print("b_to_b")
        pprint(b_to_b, width=40)

        print("to_end")
        pprint(to_end, width=40)
        exit(0)

    paths = []

    print("find_path")
    print()

    paths.append(direct_path(direct, start, steps))

    return paths[0][2]

###############################
######## EXITING EARLY ########
###############################

    print("from_start")
    pprint(from_start, width=32)

    # from start to bubble
    for f_pair, f_list in from_start.items():
        print("f_pair", f_pair, "f_list", f_list)

        start_node = f_pair[0]
        start_bubble = f_pair[1]
        new_cost = len(f_list) * 2  # cost is 2 per node
        print(
            "start_node", start_node,
            "start_bubble", start_bubble,
        )

        # from bubble_entry to bubble_exit
        for b_node, b_list in b_to_b.items():
            print("b_node", b_node, "b_list", b_list)

            # looking for the tunnel start
            if b_node[0] != start_bubble:
                print("...skipped")
                continue

            bubble_entry = b_node[0]  # entry bubble
            bubble_exit = b_node[1]  # exit bubble
            new_cost += len(b_list)  # cost is 1 per node
            print(
                "bubble_entry", bubble_entry,
                "bubble_exit", bubble_exit,
            )

            # from bubble_exit to end
            for e, e_list in to_end.items():
                e0 = e[0]
                end_node = e[1]
                print("e0", e0, "end_node", end_node, "e_list", e_list)

                if e0 != bubble_exit:
                    print("...skipped")
                    continue

                new_cost += len(e_list) * 2  # cost is 2 per node
                print(
                    "start_node", start_node,
                    "bubble_entry", bubble_entry,
                    "bubble_exit", bubble_exit,
                    "end_node", end_node,
                    "new_cost", new_cost
                )

    return "RRRDDD"

if __name__ == "__main__":

    steps = {
        ((0, 0), (0, 1)): 'R',
        ((0, 0), (1, 0)): 'D',
        ((0, 1), (0, 0)): 'L',
        ((0, 1), (0, 2)): 'R',
        ((0, 1), (1, 1)): 'D',
        ((0, 2), (0, 1)): 'L',
        ((0, 2), (0, 3)): 'R',
        ((0, 2), (1, 2)): 'D',
        ((0, 3), (0, 2)): 'L',
        ((0, 3), (1, 3)): 'D',
        ((1, 0), (0, 0)): 'U',
        ((1, 0), (1, 1)): 'R',
        ((1, 0), (2, 0)): 'D',
        ((1, 1), (0, 1)): 'U',
        ((1, 1), (1, 0)): 'L',
        ((1, 1), (1, 2)): 'R',
        ((1, 1), (2, 1)): 'D',
        ((1, 2), (0, 2)): 'U',
        ((1, 2), (1, 1)): 'L',
        ((1, 2), (1, 3)): 'R',
        ((1, 2), (2, 2)): 'D',
        ((1, 3), (0, 3)): 'U',
        ((1, 3), (1, 2)): 'L',
        ((1, 3), (2, 3)): 'D',
        ((2, 0), (1, 0)): 'U',
        ((2, 0), (2, 1)): 'R',
        ((2, 0), (3, 0)): 'D',
        ((2, 1), (1, 1)): 'U',
        ((2, 1), (2, 0)): 'L',
        ((2, 1), (2, 2)): 'R',
        ((2, 1), (3, 1)): 'D',
        ((2, 2), (1, 2)): 'U',
        ((2, 2), (2, 1)): 'L',
        ((2, 2), (2, 3)): 'R',
        ((2, 2), (3, 2)): 'D',
        ((2, 3), (1, 3)): 'U',
        ((2, 3), (2, 2)): 'L',
        ((2, 3), (3, 3)): 'D',
        ((3, 0), (2, 0)): 'U',
        ((3, 0), (3, 1)): 'R',
        ((3, 1), (2, 1)): 'U',
        ((3, 1), (3, 0)): 'L',
        ((3, 1), (3, 2)): 'R',
        ((3, 2), (2, 2)): 'U',
        ((3, 2), (3, 1)): 'L',
        ((3, 2), (3, 3)): 'R',
        ((3, 3), (2, 3)): 'U',
        ((3, 3), (3, 2)): 'L'
    }

    direct = [(3, 3), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]

    start = (0, 0)

    end = (3, 3)

    from_start = {
        ((0, 0), (2, 0)): [(2, 0), (1, 0)],
        ((0, 0), (2, 3)): [(2, 3), (1, 3), (0, 3), (0, 2), (0, 1)]
    }

    b_to_b = {
        ((2, 0), (2, 3)): [(2, 3), (1, 3), (1, 2), (1, 1), (2, 1)],
        ((2, 3), (2, 0)): [(2, 0), (1, 0), (1, 1), (1, 2), (1, 3)]}

    to_end = {
        ((2, 0), (3, 3)): [(3, 3), (2, 3), (1, 3), (1, 2), (1, 1), (2, 1)],
        ((2, 3), (3, 3)): [(3, 3)]
    }

    find_path(steps, direct, start, end, from_start, b_to_b, to_end)

# end of file
