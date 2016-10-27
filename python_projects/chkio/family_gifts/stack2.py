# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

########################################################################

from __future__ import print_function

########################################################################

from collections import defaultdict, deque
from pprint import pformat, pprint
from calc_gifts import calc_gifts

########################################################################

DEBUG = False

########################################################################


def normalize(path, family0):
    """Rotate the circular path to have 'family0' at the start."""
    d = deque(path)
    if family0 not in d:
        return path

    while d[0] != family0:
        d.rotate(-1)

    return list(d)

########################################################################


# def unwrap(dictionary_list, n0):
#     """Unwrap the solution list of dictionaries, starting each with n0."""
#     out = []
#     for solution_dict in dictionary_list:
#         result = [n0]
#         next = solution_dict[n0]
#         while next != n0:
#             result.append(next)
#             next = solution_dict[next]
#         if DEBUG:
#             print(result)
#         out.append(tuple(result))
#     return out

########################################################################


def remove_pairs(pairs, p):
    """Remove elements from p that contain elements in pairs."""
    removables = []
    for pair in pairs:
        removables.extend([x for x in p if x.find(pair) != -1])
    removables = set(removables)

    if DEBUG:
        print(
            "remove_pairs",
            pformat(pairs),
            len(p),
            "-",
            len(removables),
            "=",
            len(p) - len(removables)
        )

    for match in removables:
        p.remove(match)

########################################################################


def find_chain(family, couples, paths=[]):
    """Find a chain of gift-givers in 'family', excluding 'couples'."""
    """Members of 'family' give gifts to each other each year; pairs of members
    that are 'couples' don't give to each other. Compute the chains of giving
    such that no member gives to the same person in another chain."""
    # form the blacklist, pairs of people who cannot exchange gifts
    blacklist = defaultdict(list)
    for x, y in couples:
        blacklist[x].append(y)
        blacklist[y].append(x)

    # add to the blacklist to reflect previous paths
    for path in paths:
        for k, v in path.items():
            if v not in blacklist[k]:
                blacklist[k].append(v)

    if DEBUG:
        print("blacklist", pformat(dict(blacklist), width=132))

    # convert set to list
    names = list(family)

    return calc_gifts(names, blacklist)

########################################################################


def unwind(solution_dict, n0):
    """Convert path dictionary to a list beginning with 'n0'."""
    result = [n0]
    next = solution_dict[n0]
    while next != n0:
        result.append(next)
        next = solution_dict[next]
    if DEBUG:
        print(result)
    return result

########################################################################

family = {
    'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
    'Maryanne', 'Penny', 'Matthew'
}

couples = (
    {"Loraine", "Benjamin"},
    {"Leah", "Matthew"},
    {"Todd", "Jenifer"},
)

# change couples from sets to tuples
couples = [tuple(sorted([x, y])) for (x, y) in couples]

# get the first name in the family
n0 = sorted(list(family))[0]

good_paths = []
generator = find_chain(family, couples, good_paths[:])
# print(next(generator))

chains = list(generator)
print(len(chains))

len_family = len(family)
full_chains = [x for x in chains if len(unwind(x, n0)) == len_family]
print(len(full_chains))


# solutions = list(generator)
# print(
#     pformat(
#         [
#             long_enough for long_enough in
#             [
#                 unwind(path, n0) for path in generator
#             ] if len(long_enough) == len(family)
#         ],
#         width=288
#     )
# )
#
# try:
#     good_paths = []
#     generator = find_chain(family, couples, good_paths[:])
#     while 1:
#         path = next(generator)
#         print("pre-unwind", pformat(path))
#         upath = unwind(path, n0)
#         print(len(upath), pformat(upath, depth=2))
#         if len(upath) == len(family):
#             good_paths.append(path)
#             generator = find_chain(family, couples, good_paths[:])
#
# except StopIteration:
#     pass
#
# print(72 * '#')
# print(len(good_paths))
#
# for path in good_paths:
#     pprint(unwind(path, n0), width=288)
#
# print(72 * '#')
#
# bogus = [
#     [('Benjamin', 'Jenifer'), ('Jenifer', 'Leah'), ('Leah', 'Loraine'), ('Loraine', 'Maryanne'), ('Maryanne', 'Matthew'), ('Matthew', 'Penny'), ('Penny', 'Russell'), ('Russell', 'Todd'), ('Todd', 'Benjamin')],
#     [('Benjamin', 'Todd'), ('Todd', 'Russell'), ('Russell', 'Jenifer'), ('Jenifer', 'Loraine'), ('Loraine', 'Leah'), ('Leah', 'Maryanne'), ('Maryanne', 'Penny'), ('Penny', 'Matthew'), ('Matthew', 'Benjamin')],
#     [('Benjamin', 'Matthew'), ('Matthew', 'Jenifer'), ('Jenifer', 'Maryanne'), ('Maryanne', 'Leah'), ('Leah', 'Penny'), ('Penny', 'Todd'), ('Todd', 'Loraine'), ('Loraine', 'Russell'), ('Russell', 'Benjamin')],
#     [('Benjamin', 'Russell'), ('Russell', 'Leah'), ('Leah', 'Todd'), ('Todd', 'Maryanne'), ('Maryanne', 'Jenifer'), ('Jenifer', 'Matthew'), ('Matthew', 'Loraine'), ('Loraine', 'Penny'), ('Penny', 'Benjamin')],
#     [('Benjamin', 'Maryanne'), ('Maryanne', 'Todd'), ('Todd', 'Matthew'), ('Matthew', 'Russell'), ('Russell', 'Loraine'), ('Loraine', 'Jenifer'), ('Jenifer', 'Penny'), ('Penny', 'Leah'), ('Leah', 'Benjamin')],
#     [('Benjamin', 'Penny'), ('Penny', 'Loraine'), ('Loraine', 'Matthew'), ('Matthew', 'Todd'), ('Todd', 'Leah'), ('Leah', 'Jenifer'), ('Jenifer', 'Russell'), ('Russell', 'Maryanne'), ('Maryanne', 'Benjamin')],
#     [('Benjamin', 'Leah'), ('Leah', 'Russell'), ('Russell', 'Matthew'), ('Matthew', 'Maryanne'), ('Maryanne', 'Loraine'), ('Loraine', 'Todd'), ('Todd', 'Penny'), ('Penny', 'Jenifer'), ('Jenifer', 'Benjamin')]
# ]
#
# for path in sorted(bogus):
#     pprint([x[0] for x in path], width=288)
#
# end of file
