# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/family-gifts/

# http://algohangout.blogspot.com/2015/01/ \
#   graphtheory-using-python.html?view=sidebar

from __future__ import print_function

########################################################################

from pprint import pformat

########################################################################


def findAllPaths(g, start, end, path=[]):
    if path == []:
        print(
            "\n\nfindAllPaths",
            "\n  g", pformat(g),
            "\n  start", pformat(start),
            "\n  end", pformat(end),
            "\n  path", pformat(path)
        )

    path = path + [start]

    if start == end:
        return [path]

    if start not in g:
        return []

    paths = []

    for node in g[start]:

        if node not in path:
            newpaths = findAllPaths(g, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths

########################################################################

if __name__ == "__main__":

    if 0:

        g = {0: [1, 2, 3], 1: [3], 2: [0, 1], 3: []}

        assert findAllPaths(g, 2, 3) == [
            [2,  0,  1,  3],
            [2,  0,  3],
            [2,  1,  3]
        ], "Test failed"

    # output: [[2,  0,  1,  3],  [2,  0,  3],  [2,  1,  3]]

########################################################################

    g = {
        'Javier': ['Curtis', 'Lee'],
        'Curtis': ['Javier', 'Rachel'],
        'Lee': ['Javier', 'Rachel'],
        'Rachel': ['Curtis', 'Lee']
    }

    print(findAllPaths(g, 'Javier', 'Curtis'))
    print(findAllPaths(g, 'Javier', 'Lee'))
    print(findAllPaths(g, 'Javier', 'Rachel'))

    print(findAllPaths(g, 'Curtis', 'Lee'))
    print(findAllPaths(g, 'Curtis', 'Rachel'))

    print(findAllPaths(g, 'Lee', 'Rachel'))

#   g = {
#       'Javier': ['Lee', 'Curtis'],
#       'Curtis': ['Javier', 'Rachel'],
#       'Lee': ['Rachel', 'Javier'],
#       'Rachel': ['Curtis', 'Lee']
#   }
# end of file
