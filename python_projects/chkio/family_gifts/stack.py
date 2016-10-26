# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

"""Search for family gift lists."""

# https://py.checkio.org/mission/family-gifts/

########################################################################

from __future__ import print_function

########################################################################

from collections import defaultdict, deque
from pprint import pformat, pprint

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

# http://stackoverflow.com/questions/13089352/
#   how-can-i-figure-out-who-can-give-gifts-to-whom-on-christmas


def calc_gifts(names, blacklist, gifts={}):
    """Calculate gift circles."""
    if len(names) > 0:
        name, rest = names[0], names[1:]
        for other in names + list(gifts):
            if (other != name and
                    other not in blacklist[name] and
                    (other not in gifts or gifts[other] != name) and
                    other not in gifts.values()):

                gifts_new = dict(gifts.items() + [(name, other)])
                for solution in calc_gifts(rest, blacklist, gifts_new):
                    yield solution
    else:
        yield gifts

########################################################################


def unwrap(dictionary_list, n0):
    """Unwrap the solution list of dictionaries, starting each with n0."""
    out = []
    for solution_dict in dictionary_list:
        result = [n0]
        next = solution_dict[n0]
        while next != n0:
            result.append(next)
            next = solution_dict[next]
        if DEBUG:
            print(result)
        out.append(tuple(result))
    return out

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

    return next(calc_gifts(names, blacklist))

########################################################################


def unwind(solution_dict, n0):
    result = [n0]
    next = solution_dict[n0]
    while next != n0:
        result.append(next)
        next = solution_dict[next]
    if DEBUG:
        print(result)
    return result

########################################################################



# def old_find_chains(family, couples):
#     """Find chains of gift-givers in 'family', excuding 'couples'.
#
#     Members of 'family' give gifts to each other each year; pairs of members
#     that are 'couples' don't give to each other. Compute the chains of giving
#     such that no member gives to the same person in another chain."""
#
#     # form the blacklist, pairs of people who cannot exchange gifts
#     blacklist = defaultdict(list)
#     for x, y in couples:
#         blacklist[x].append(y)
#         blacklist[y].append(x)
#
#     # convert set to list
#     names = list(family)
#
#     # get the alphabetically first name
#     name0 = sorted(names)[0]
#
#     # compute all chains, starting them with name0
#     solution = unwrap(
#         list(
#             calc_gifts(names, blacklist)
#         ),
#         name0
#     )
#
#     # keep chains of family length
#     solution = set([x for x in solution if len(x) == len(family)])
#
#     if 1 or DEBUG:
#         print("solution", pformat(solution))
#
#     # keep only the chains having different pairings from one another
#     chains = []
#
#     # form a list of solution strings
#     p = list([" ".join(list(x)) for x in solution])
#     while p:
#         # get the topmost solution
#         r0 = (p.pop(0)).split()
#         if DEBUG:
#             print("\nr0", r0)
#
#         # add this solution to the output
#         chains.append(
#             normalize(
#                 r0,
#                 name0
#             )
#         )
#
#         # form gift-giving pairs
#         c0 = r0 + [r0[0]]
#         pairs = [" ".join(c0[i:i + 2]) for i in range(len(c0) - 1)]
#         if DEBUG:
#             print("\npairs", pformat(pairs))
#         remove_pairs(pairs, p)
#
#     if DEBUG:
#         print("chains", "\n", len(chains), "\n", pformat(chains, width=132))
#
#     return chains

########################################################################

# assert len(
#     find_chains(
#         {"Allison", "Robin", "Petra", "Curtis", "Bobbie", "Kelly"},
#         (
#             {"Allison", "Curtis"},
#             {"Robin", "Kelly"},
#         )
#     )
# ) == 4

# if 0:
#     family = {'Philip', 'Sondra', 'Mary', 'Selena', 'Eric', 'Phyllis'}
#     couples = (
#         {'Philip', 'Sondra'},
#         {'Eric', 'Mary'},
#     )
#
#     find_chains(family, couples)
#
# else:

family = {
    'Loraine', 'Leah', 'Jenifer', 'Russell', 'Benjamin', 'Todd',
    'Maryanne', 'Penny', 'Matthew'
}

couples = (
    {"Loraine", "Benjamin"},
    {"Leah", "Matthew"},
    {"Todd", "Jenifer"},
)

# family = {"Allison", "Robin", "Petra", "Curtis", "Bobbie", "Kelly"}
# couples = ({"Allison", "Curtis"}, {"Robin", "Kelly"},)

# convert from sets to tuples
pprint(couples)
couples = [tuple(sorted([x, y])) for (x, y) in couples]
pprint(couples)

n0 = sorted(list(family))[0]

try:
    good_paths = []
    bad_paths = []
    while 1:
        path = find_chain(family, couples, good_paths[:] + bad_paths[:])
        print("pre-unwind", pformat(path))
        upath = unwind(path, n0)
        print(len(upath), pformat(upath, depth=2))
        if len(upath) == len(family):
            good_paths.append(path)
        else:
            bad_paths.append(path)
except StopIteration:
    pass

print(72 * '#')
print(len(good_paths))

for path in good_paths:
    pprint(path, width=132)


# end of file
