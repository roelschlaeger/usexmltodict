# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/probably-dice/
# http://mathworld.wolfram.com/Dice.html

from math import factorial, floor


def choose(n, k):
    """Compute (n)
               (k)
    """
    return factorial(n) / (factorial(k) * factorial(n - k))


def compute_product(points, number_of_dice, sides_per_die):
    """Compute the number of product terms for a given number of points."""

    limit = int(floor((points - number_of_dice) / sides_per_die))

    sum = 0
    for k in range(limit + 1):

        mult = -1 if (k & 1) else 1

        n_by_k = choose(number_of_dice, k)
        p_sk_1 = choose(points - sides_per_die * k - 1, number_of_dice - 1)
        sum += mult * n_by_k * p_sk_1

    return sum


def probability(number_of_dice, sides_per_die, target_number):
    """Compute the probability of a given target_number given the number of
dice and the number of sides."""

    if number_of_dice * sides_per_die < target_number:
        return 0

    c = compute_product(target_number, number_of_dice, sides_per_die)
    grand_total = sides_per_die ** number_of_dice
    result = round(float(c) / float(grand_total), 4)
    return result

assert probability(2, 6, 3) == 0.0556  # 2 six-sided dice have a 5.56% chance of totalling 3
assert probability(2, 6, 4) == 0.0833
assert probability(2, 6, 7) == 0.1667
assert probability(2, 3, 5) == 0.2222  # 2 three-sided dice have a 22.22% chance of totalling 5
assert probability(2, 3, 7) == 0       # The maximum you can roll on 2 three-sided dice is 6
assert probability(3, 6, 7) == 0.0694
assert probability(10, 10, 50) == 0.0375

print("Done!")

# end of file
