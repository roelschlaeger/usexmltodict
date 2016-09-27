# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

#https://py.checkio.org/mission/morse-clock/

from __future__ import print_function


def binary(n, w):
    """Convert 'number' to a binary string of width 'w'."""
    number = n
    out = []
    for _ in range(w):
        number, d = divmod(number, 2)
        out.append('.' if d == 0 else '-')
    out.reverse()
    result = "".join(out)
#   print(n, w, result)
    return result


def checkio(s):
    """Output the time string in 's' in a compact Morse format.

    Input format for s:

        hh:mm:ss  normal       length:8
        h:m:s     missing 0's  length:5
        hh:m:ss   missing 0's  length:7

    where:
        0 <= hh <= 23
        0 <= mm <= 59
        0 <= ss <= 59
    """

    # rewrite the string to the 'normal' format, putting back missing 0's
    h, m, s = map(int, s.split(":"))
    s = "%02d:%02d:%02d" % (h, m, s)

    # width of each output field in bits
    bits = [2, 4, 0, 3, 4, 0, 3, 4]

    out = []

    for index, c in enumerate(s):
        if c == ":":
            out.append(":")
        else:
            d = int(c)
            out.append(binary(d, bits[index]))

    result = " ".join(out)
#   print(result)
    return result


assert checkio("10:37:49") == ".- .... : .-- .--- : -.. -..-"
assert checkio("21:34:56") == "-. ...- : .-- .-.. : -.- .--."
assert checkio("00:1:02") == ".. .... : ... ...- : ... ..-."
assert checkio("23:59:59") == "-. ..-- : -.- -..- : -.- -..-"
print("Done!")

