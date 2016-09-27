# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/most-numbers/


def checkio(*numbers):
    if not numbers:
        result = 0
    else:
        numbers = sorted(numbers)
        result = round(numbers[-1] - numbers[0], 3)
    return result


assert checkio(1, 2, 3) == 2
assert checkio(5, -5) == 10
assert checkio(10.2, -2.2, 0, 1.1, 0.5) == 12.4
assert checkio() == 0
print("Done!")
