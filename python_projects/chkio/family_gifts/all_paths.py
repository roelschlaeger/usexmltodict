# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

from __future__ import print_function

########################################################################

from collections import defaultdict
# from pprint import pformat

########################################################################

EDGES = [
    ('Alex', 'Beth'),
    ('Alex', 'Lee'),

    ('Beth', 'Curtis'),
    ('Beth', 'Javier'),
    ('Beth', 'Lee'),
    ('Beth', 'Rachel'),

    ('Curtis', 'Javier'), ('Curtis', 'Rachel'),

    ('Javier', 'Curtis'), ('Javier', 'Lee'),

    ('Lee', 'Javier'), ('Lee', 'Rachel'),

    ('Rachel', 'Curtis'), ('Rachel', 'Lee')
]

########################################################################


def make_graph(edges):
    graph = defaultdict(list)
    for f, t in edges:
        graph[f].append(t)
    return graph


########################################################################


def find_all_paths(graph, start, end, path=[]):
#   if path == []:
#       print(
#           "\ngraph", pformat(graph),
#           "\nstart", start,
#           "\nend", end,
#           "\npath", path,
#       )

    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths

########################################################################


def find_n_length_paths(n, graph, start, end):
    return [x for x in find_all_paths(graph, start, end) if len(x) == n]

########################################################################


def chains(edges):

    graph = make_graph(edges)

    # collect all vertex names
    m = sorted(set([x[0] for x in edges]))
    print("\n\nm", m)

    from collections import Counter
    c = Counter([x[0] for x in edges])
    print("\nc", c)

    output = []

    for m0 in m:

        partners = graph[m0]
        print(
            "\nm0", m0,
            "\npartners", partners
        )

        result = set()

        for partner in partners:
            # print("\n\npartner", partner)
            paths = find_n_length_paths(len(m), graph, m0, partner)
            for path in paths:
                # print(
                #     "\nlen(path)", len(path),
                #     "\npath", path
                # )
                if len(path) == len(m):
                    result.add(tuple(path))

        print(len(result), m0, result)
        output.append((len(result), m0, result))

    return max(output)

########################################################################

result = chains(EDGES)
print(
    "\n\nlen(result)", len(result),
    "\nresult", result
)

# end of file
