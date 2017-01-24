"""Continued fraction expansion."""

from __future__ import print_function


def convert(n, d):
    """Expand n/d to a continued fraction."""

    # isolate integer and fractional portions of result
    i, n = divmod(n, d)

    # set up data structures
    qlist = []  # list of successive quotient digits
    remainders = {}  # dictionary of qlist location of remainder

    while n not in remainders:
        # mark the location of the remainder
        remainders[n] = len(qlist)
        # compute one more digit of the quotient
        q, n = divmod(n * 10, d)
        # save the quotient digit as a string
        qlist.append(str(q))

    # locate the start of the repeat
    r = remainders[n]
    # concatenate the integer and fixed fractional part
    result = "%s." % i + "".join(qlist[:r])
    # compute the repeated fraction
    frac = "(" + "".join(qlist[r:]) + ")"
    # don't append the repeated '0' series
    if frac != "(0)":
        result += frac

    return result

if __name__ == '__main__':
    print(convert(1, 1))
    print(convert(1, 2))
    print(convert(1, 3))
    print(convert(1, 4))
    print(convert(1, 5))
    print(convert(1, 6))
    print(convert(1, 7))
    print(convert(1, 8))
    print(convert(1, 9))
    print(convert(1, 10))
    print(convert(1, 11))
    print(convert(1, 12))
    print(convert(1, 13))
    print(convert(1, 97))
    print(convert(1, 970))
    print(convert(1, 9700))
    print(convert(1, 97000))

# end of file
