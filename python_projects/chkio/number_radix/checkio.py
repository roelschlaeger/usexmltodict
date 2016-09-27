# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/number-radix/


DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def checkio(s, radix):
    """Convert the digits string 's' in radix base to decimal."""
    charset = DIGITS[:radix]

    result = 0
    for c in list(s.upper()):
        d = charset.find(c)
        if d == -1:
            return -1
        result = result * radix + charset.index(c)

    return result

checkio("AF", 16) == 175
checkio("101", 2) == 5
checkio("101", 5) == 26
checkio("Z", 36) == 35
checkio("AB", 10) == -1
print("Done!")

# end of file
