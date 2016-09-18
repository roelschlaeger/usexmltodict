"""Convert number in the range 0 <= n <= 3999 to a Roman numeral."""

values = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
]


def checkio(n):
    """Convert n to a Roman numeral string."""
    out = []
    for v, s in values:
        while v <= n:
            n -= v
            out.append(s)
    return "".join(out)

assert checkio(6) == 'VI'
assert checkio(76) == 'LXXVI'
assert checkio(13) == 'XIII'
assert checkio(44) == 'XLIV'
assert checkio(3999) == 'MMMCMXCIX'
