# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/friendly-number/

from __future__ import print_function


def friendly_number(
    n,
    base=1000,
    decimals=0,
    suffix="",
    powers=['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
):
    """Return a string representing a number in a 'friendly' format."""

    number = float(abs(n))
    base = float(base)

    shifts = 0
    while (number >= base) and (shifts < (len(powers) - 1)):
        number /= base
        shifts += 1

    if decimals == 0:
        from math import floor
        number = floor(number)

    if n < 0:
        number = -number

    number = "%.*f" % (decimals, round(number, decimals))
    out = str(number) + powers[shifts] + suffix

    print(n, base, decimals, suffix, powers, ":", out)

    return out


assert friendly_number(102) == '102'
assert friendly_number(10240) == '10k'
assert friendly_number(12341234, decimals=1) == '12.3M'
assert friendly_number(12000000, decimals=3) == '12.000M'
assert friendly_number(12461, decimals=1) == '12.5k'
assert friendly_number(1024000000, base=1024, suffix='iB') == '976MiB'
assert friendly_number(-150, base=100, powers=['', 'd', 'D']) == '-1d'
assert friendly_number(-155, base=100, decimals=1, powers=['', 'd', 'D']) == '-1.6d'
assert friendly_number(255000000000, powers=['', 'k', 'M']) == '255000M'
print("Done!")
