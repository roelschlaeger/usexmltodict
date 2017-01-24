# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/repeating-decimals/

from __future__ import print_function

########################################################################

from fractions import Fraction

########################################################################


def convert(n, d):
    f0 = Fraction(n, d)

    f1 = f0.limit_denominator()

    sign = (f1.numerator < 0)
    if sign:
        f1 = - f1
    integer_part = int(f1)

    n = f1.numerator - integer_part * f1.denominator
    d = f1.denominator

    f2 = Fraction(n, d)

    print("\nconvert",
          "\n  n", n,
          "\n  d", d,
          "\n  f0.numerator", f0.numerator,
          "\n  f0.denominator", f0.denominator,
          "\n  sign", sign,
          "\n  integer_part", integer_part,
          "\n  f2.numerator", f2.numerator,
          "\n  f2.denominator", f2.denominator
          )

    dividend = 1000000000000000000 * f2.numerator
    s = str(int(dividend / f2.denominator))
    print(s)
    found = False
    for i in range(len(s) - 1, 0, -1):
        ss = s[:i]
        if ss in s[i:]:

            print(
                "\n  s.find(ss)", s.find(ss),
                "\n  i", i,
                "\n  ss", ss,
                "\n  s[i:]", s[i:]
            )
            if not found:
                found = True
                leading_fraction = s[:i] if i > 0 else ""
                repeating_fraction = "(" + ss + ")"
                print(
                    "\n\n  leading_fraction", leading_fraction,
                    "\nrepeating_fraction", repeating_fraction
                )

    fractional_part = leading_fraction + repeating_fraction
    result = "%(integer_part)s.%(fractional_part)s" % locals()
    print("result", result)
    import sys
    sys.exit(0)

########################################################################

# convert(1000, 1001)
convert(8, 7) == "1.(142857)"
convert(1, 3) == "0.(3)"
convert(5, 3) == "1.(6)"
convert(3, 8) == "0.375"
convert(7, 11) == "0.(63)"
convert(29, 12) == "2.41(6)"
convert(11, 7) == "1.(571428)"
convert(0, 117) == "0."
convert(4, 2) == "2."

# convert(1, 3) == "0.(3)"
# convert(5, 3) == "1.(6)"
# convert(3, 8) == "0.375"
# convert(7, 11) == "0.(63)"
# convert(29, 12) == "2.41(6)"
# convert(11, 7) == "1.(571428)"
# convert(0, 117) == "0."
# convert(4, 2) == "2."
# end of file
