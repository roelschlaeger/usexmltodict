"""Find the median of a list of numbers"""


def checkio(l):
    """Find the median of a list of numbers."""
    n = len(l)
    if (n & 1):
        return sorted(l)[n // 2]
    else:
        return sum(sorted(l)[(n // 2) - 1: (n // 2) + 1]) / 2.


assert checkio([1, 2, 3, 4, 5]) == 3
assert checkio([3, 1, 2, 5, 3]) == 3
assert checkio([1, 300, 2, 200, 1]) == 2
assert checkio([3, 6, 20, 99, 10, 15]) == 12.5

print("Done")
