# https://py.checkio.org/mission/restricted-sum/

# Given a list of numbers, you should find the sum of these numbers. Your
# solution should not contain any of the banned words, even as a part of
# another word.
#
# The list of banned words are as follows:
#
# sum
# import
# for
# while
# reduce


# must be python2

def checkio(l):
    """Compute a restricted s-u-m."""

    def add2a(b, a={"s": 0}):
        a["s"] += b
        return a["s"]

    map(add2a, l)
    return add2a(0)


assert checkio([1, 2, 3]) == 6
assert checkio([2, 2, 2, 2, 2, 2]) == 12
assert checkio(range(21)) == 210
assert checkio(range(101)) == 5050
print("Done!")
