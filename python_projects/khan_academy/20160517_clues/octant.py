"""Convert octant cipher in 9210801046_586c49b847_c.jpg to alphabet."""

from __future__ import print_function
from collections import Counter
import string

"""The octant cipher is an arbitrary encodinng of the symbols found in the
picture from Khan Academy.

The digits in the cipher are assigned beginning with

- '1' being a vertical
- '2' being at 1:30 o'clock
- '3' being at 3:00 o'clock
- '4' being at 4:30 o'clock
- '5' being at 6:00 o'clock
- '6' being at 7:30 o'clock
- '7' being at 9:00 o'clock
- '8' being at 10:30 o'clock

The lesser of the two symbols in a pair is the smaller number
"""

SYMBOLS = """
4527585614274716184558187845362712471278121458162725
25341258232345163612584545455827452325232758
4727164556343836147825235818143467182745671238
1636277825181614783434361634256734181447256734
121216182718255647381238581412236714343656122518
45231878476725274518382747144738472312161212
255818474512582578251818674525234718
"""

if __name__ == "__main__":

    if 0:

        JSYMBOLS = "".join(SYMBOLS.split("\n"))
        print(len(JSYMBOLS))
        print(JSYMBOLS)
        print()

        def decode_line3(s):
            """Decode all quads of characters in s."""
            out = []
            while s:
                c1, c2, c3, s = s[0], s[1], s[2], s[3:]
                out.append(int("%c%c%c" % (c1, c2, c3)))
            return out

        def decode_lines3(lines):
            """Decode all text lines in lines."""
            out = []
            for s in lines.split("\n"):
                if not s:
                    continue
                out.extend(decode_line3(s))
            return out

        result = decode_lines3(JSYMBOLS)
        print(result)
        print()
        print(Counter(result))
        print()
        print('#' * 72)
        print()
        import sys
        sys.exit(1)

    def decode_line(s):
        """Decode all pairs of characters in s."""
        out = []
        while s:
            c1, c2, s = s[0], s[1], s[2:]
            assert (c1 < c2), "Ordering error: %s %s" % (c1, c2)
            out.append(int("%c%c" % (c1, c2)))
        # print out
        return out

    def decode_lines(lines):
        """Decode all text lines in lines."""
        out = []
        for s in lines.split("\n"):
            if not s:
                continue
            out.extend(decode_line(s))
        return out


    def create_alphabet(sym_list):
        """Create an alphabet from the symbols list."""
        def char_generator(d):
            """Generate the next available character."""
            s = string.uppercase

            # remove characters already assigned
            for c in d.values():
                s = s.replace(c, "")

            for c in s.lower():
                yield c

        """
        Counter(
            {
                12: 15,
                18: 15,
                45: 14,
                25: 13,
                27: 12,
                47: 11,
                58: 11,
                34: 9,
                14: 9,
                23: 9,
                16: 8,
                67: 7,
                78: 7,
                36: 6,
                38: 6,
                56: 4,
                68: 1,
                26: 1
            }
        )
        """

        alphabet = {
            12: 'E',
            18: 'T',
            45: 'A',
            25: 'O',
            27: 'I',
            47: 'N',
            58: 'S',
            34: 'H',
            14: 'R',
            23: 'D',
            16: 'L',
            67: 'C',
            78: 'U',
            36: 'M',
            38: 'W',
            56: 'F',
            68: 'G',
            26: 'Y',
        }
        chargen = char_generator(alphabet)
        out = []
        for n in sym_list:
            if n not in alphabet:
                alphabet[n] = chargen.next()
            out.append(alphabet[n])

        print("Alphabet")
        for k, v in sorted(alphabet.items()):
            print("%s: %s" % (k, v))
        print()

        return "".join(out)

    result = decode_lines(SYMBOLS)
    print(result)
    print()
    cr = Counter(result)
    print(len(cr), "Symbols, with this frequency:")
    print(cr)
    print()

    s = create_alphabet(result)
    c = Counter(s)
    from pprint import pprint
    pprint(c)
    print()
    for k, v in c.items():
        print("%s: %d" % (k, v))
    print(s)

# end of file
