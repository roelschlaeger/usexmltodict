# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/expected-dice/

from __future__ import print_function
from collections import defaultdict
from fractions import Fraction
from itertools import product
from string import digits, ascii_lowercase
from pprint import pprint

########################################################################


def expected(n, sides, target, l):

    die = Fraction(1, sides)
    print(die)

    board_length = len(l)
    board = [Fraction(0) for x in range(board_length)]
    print(board)
    for index, skips in enumerate(l):
        dest = (index + skips) % board_length
        board[dest] += die
    print(board)

    a = board[target]
    result = Fraction(a.denominator, a.numerator)
    print(result)
    return round(result, 1)

########################################################################


def frequencies(n, sides):
    """Returns a dictionary of (value, fraction)."""

    print("frequencies",
          "\nn", n,
          "\nsides", sides
          )

    frequency_dict = {}
    total_counts = sides ** n

    # for one die, all results are equally likely
    if n == 1:

        for face in range(1, sides + 1):
            frequency_dict[face] = Fraction(1, total_counts)

    else:

        # for more than one die, compute the results
        counts = defaultdict(lambda: 0)

        # sides are numbered beginning at 1
        symbols = range(1, sides + 1)

        # generate all rolls
        rolls = list(product(symbols, repeat=n))

        for roll in rolls:
            value = 0
            for digit in roll:
                value += digit
            counts[value] += 1

        for key in sorted(counts.keys()):
            frequency_dict[key] = Fraction(counts[key], total_counts)

    return frequency_dict

# pprint(frequencies(1, 4))
# pprint(frequencies(1, 6))
# pprint(frequencies(1, 10))
# pprint(frequencies(1, 20))

# pprint(frequencies(2, 4))
# pprint(frequencies(2, 6))
# pprint(frequencies(2, 10))
# pprint(frequencies(2, 20))

# pprint(frequencies(3, 4))
# pprint(frequencies(3, 6))
# pprint(frequencies(3, 10))
# pprint(frequencies(3, 20))

# pprint(frequencies(4, 4))
# pprint(frequencies(4, 6))
# pprint(frequencies(4, 10))
# pprint(frequencies(4, 20))

# import sys
# sys.exit()

########################################################################

if __name__ == "__main__":

    # On these first three, you have a 1/4 chance of reaching the target
    # on every roll, so on average it will take 4 rolls.
    assert expected(1, 4, 3, [0, 0, 0, 0]) == 4.0
    assert expected(1, 4, 1, [0, 0, 0, 0]) == 4.0
    assert expected(1, 4, 3, [0, -1, -2, 0]) == 4.0

    # You have a 3/4 chance of reaching the exit and 1/4 chance of ending up
    # where you started
    assert expected(1, 4, 3, [0, 2, 1, 0]) == 1.3
    assert expected(1, 6, 1, [0] * 10) == 8.6
    assert expected(2, 6, 1, [0] * 10) == 10.2

# end of file
