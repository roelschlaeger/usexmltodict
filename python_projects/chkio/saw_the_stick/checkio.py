# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/stick-sawing/

from __future__ import print_function

from pprint import pprint


def checkio(n):
    pass

N = 50

if __name__ == "__main__":

    triangle = {}
    for n in range(2, N):
        value = n * (n - 1) / 2
        triangle[n] = value

    values = triangle.values()
    pprint(values)
    print()

    sums = {}
#   for groupsize in range(2, N):
    for groupsize in range(2, N):
        for start in range(0, N - groupsize):
            total = sum(values[start: start + groupsize])
            if total > 1000:
                break
            sums.setdefault(total, [])
            sums[total].append(values[start: start + groupsize])

    pprint(sums)
    print()
    print("master_array = ")
    print([(x, y[-1]) for (x, y) in sorted(sums.items())])
    print()


    import sys
    sys.exit()

    checkio(64) == [15, 21, 28]
    checkio(371) == [36, 45, 55, 66, 78, 91]
    checkio(225) == [105, 120]
    checkio(882) == []

# end of file
