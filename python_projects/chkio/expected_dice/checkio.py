# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/expected-dice/

from __future__ import print_function
from fractions import Fraction


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
