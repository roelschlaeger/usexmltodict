"""Compute the number of days between two dates."""

from datetime import date


def days_diff(t1, t2):
    """Compute the number of days between two dates."""
    d1 = date(*t1)
    d2 = date(*t2)
    diff = abs(d2 - d1)
    print(diff.days)
    return diff.days

assert days_diff((1982, 4, 19), (1982, 4, 22)) == 3
assert days_diff((2014, 1, 1), (2014, 8, 27)) == 238
assert days_diff((2014, 8, 27), (2014, 1, 1)) == 238
