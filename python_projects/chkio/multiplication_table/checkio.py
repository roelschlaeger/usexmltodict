# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/multiplication-table/

from __future__ import print_function


def tobin(n):
    """Convert n to an unadorned binary string."""
    return bin(n)[2:]


def b_and(bm, n):
    """Form the pseudo-AND of string bm and integer n."""
    sum = 0
    for c in bm:
        if c == '1':
            sum += n
    return sum


def b_ones(bn):
    sum = 0
    for c in bn:
        sum = sum * 2 + 1
    return sum


def b_or(bm, n, bn):
    """Form the pseudo-OR of string bm and integer n/binary string bn."""
    sum = 0
    for c in bm:
        if c == '1':
            sum += b_ones(bn)
        else:
            sum += n
    return sum


def b_not(bn):
    """Form the pseudo 1's-complement of binary string bn."""
    sum = 0
    for c in bn:
        sum = sum * 2
        if c == '0':
            sum += 1
    return sum


def b_xor(bm, n, bn):
    """Form the pseudo-XOR of string bm and integer n/binary string bn."""
    sum = 0
    not_n = b_not(bn)
    print("bn", bn, "not_n", not_n)
    for c in bm:
        if c == '0':
            sum += n
        else:
            sum += not_n
    return sum


def checkio(m, n):
    """Generate bogus multiply."""

    bm = tobin(m)
    bn = tobin(n)

    band = b_and(bm, n)
    bor = b_or(bm, n, bn)
    bxor = b_xor(bm, n, bn)

    result = band + bor + bxor
    print(m, n, band, bor, bxor, result)

    return result

if __name__ == "__main__":

    assert checkio(4, 6) == 38
    assert checkio(2, 7) == 28
    assert checkio(7, 2) == 18
    assert checkio(3, 9) == 60
    print("Done!")

# end of file
