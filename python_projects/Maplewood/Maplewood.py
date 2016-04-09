# vim:ts=4:sw=4:tw=0:wm=0:et

"""
    Search for solutions to GC341XG "It's Maple(wood)"
"""

from __future__ import print_function
from math import sqrt

# the locations for strangely colored pixels in the Maple(wood) figure
PAIRS = [
    (10,  25),
    (14, 117),
    (81,  55),
    (268,  25),
    (333, 159),
    (454, 117),

    # other interesting vertices
    #   ( 18,  55),
    #   ( 96, 159),
    #   (138,  10),
    #   (277,  55),
    #   (454,  96),
    #   (454, 144),
]

if 0:

    def compute_distances(pairs):
        for index, pair in enumerate(pairs[:-1]):
            x1, y1 = pair
            for x2, y2 in pairs[index + 1:]:
    #               if (x1==x2 and y1==y2):
    #                   continue
                d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
                d = sqrt(d2)
                print(
                    ("%6.1f: (%3d, %3d) to (%3d, %3d)") %
                    (round(d, 1), x1, y1, x2, y2)
                )

    compute_distances(PAIRS)
    import sys
    sys.exit()


def compute_nums():
    nums = []
    for pair in PAIRS:
        x, y = pair
        if x not in nums:
            nums.append(x)
        if y not in nums:
            nums.append(y)
    nums.sort()
    return nums


def compute_diffs(nums):
    results = []
    for i in range(len(nums) - 1):
        x = nums[i]
        for j in range(i + 1, len(nums)):
            y = nums[j]
            s = ("%3d %3d %3d" % (y - x, x, y))
            print(s)
            results.append(s)
    results.sort()
    print()
    print("\n".join(results))

if __name__ == "__main__":
    nums = compute_nums()
    compute_diffs(nums)
