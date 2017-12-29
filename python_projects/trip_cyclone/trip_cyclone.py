# vim:ts=4:sw=4:tw=0:wm=0:et
TEXT = """
0101010001101000011001010010000001000011011
0000101100011011010000110010100100000010011
0101100001011110010010000001101111011100100
0100000010011010110000101111001001000000100
1110011011110111010000100000011000100110010
1001000000110000101110100001000000111010001
1010000110010100100000010100000110111101110

0110111010001100101011001000010000001000011
0110111101101111011100100110010001101001011
0111001100001011101000110010101110011001011
10

010
011110110011000
100000011000
1101101111011101
010111001001110011011001010010110000001101000
0101001110100011010
0001100101011100100110010100100000011000010111001

001100101
001000
000111001
101101111011011010110010100100000010

100010111010101100101011100110111010001101
001011011110110111000100000011101000

1101111001000000100000101101110011100110111
01110110010101110010001011000010000001010
01001100101011
00110011001010111001001100
101011011100110001101100101001000000
1110000011011110110100101101110011
101000010110000100000010100
1101110100011000010110011101100101011100
1100100000011011110110011000100000
011000010000110100001010010011010
11101010110110001110100011010
010110001101100001011000110110100001100101
2C20547261696C686561
642C2061205061726B696E672061726561
2C20616E64206F6620636F75727365206120
46696E616C0D0A576179706F696E74206
F722074776F2
E00"""

# Response text from one finder
# TEXT2 = """0100100100100000011011000110111101110110011001010010000001100001001000000110011101101111011011110110010000100000011100000111010101111010011110100110110001100101001000000110000101101110011001000010000001110100011010000110100101110011001000000110111101101110011001010010000001110111011000010111001100100000011000110110010101110010011101000110000101101001011011100110110001111001001000000111010001101111011101010110011101101000001011100010000000100000010101000110111101101111001000000110110101110101011000110110100000100000011001100110111101110010001000000110110101111001001000000110110001101001011101000111010001101100011001010010000001100010011100100110000101101001011011100010110000100000011010010111010000100000011101000110000101101011011001010111001100100000011000010010000001110110011010010110110001101100011000010110011101100101001000000110000101101110011001000010000001100110011011110111001000100000011011010110010100100000011100110110111101101101011001010010000001110010011001010110000101101100011011000111100100100000011100110110110101100001011100100111010000100000011001100111001001101001011001010110111001100100011100110010111000100000001000000100111001101111011101000010000001110011011101010111001001100101001000000110100101100110001000000110010101110110011001010111001001111001011011110110111001100101001000000111011101101001011011000110110000100000011100110110000101111001001011000010000001100010011101010111010000100000010010010010011101101100011011000010000001100011011011110110111001100110011010010111001001101101001000000111010001101000011000010111010000100000010001000111001001010000011011110111011101100101011100100100001101100001011101000010000001101001011100110010000001110100011010000110010100100000011011010110000101101110001000000110111101101110001000000111010001101000011010010111001100100000011011110110111001100101001011000010000001101000011001010010000001110011011011110110110001110110011001010110010000100000011010010111010000100000011000010110111001100100001000000110110101100001011001000110010100100000011101000110100001100101001000000110011001101001011011100110010000101100001000000110100101101110001000000110000100100000011100000110110001100001011000110110010100100000010010010010011101101101001000000111000001110010011001010111010001110100011110010010000001110011011101010111001001100101001000000100100100100000011010000110000101100100001000000110110001101111011011110110101101100101011001000010111000100000001000000101010001101000011001010010000001100011011000010110001101101000011001010010000001110111011000010111001100100000011010110110100101101110011001000110000100100000011010010110111000100000011101000110100001100101001000000110011101110010011011110111010101101110011001000010110000100000010010010010000001101101011001010110000101101110001000000110100101110100001001110111001100100000011000100110010101100101011011100010000001100001001000000110001101101111011101010111000001101100011001010010000001111001011001010110000101110010011100110010000001101000011001010111001001100101001000000111001101101001011011100110001101100101001000000110100101110100001000000111011101100001011100110010000001101100011000010111001101110100001000000110011001101111011101010110111001100100001011100010000000100000010000100111010101110100001000000110100101110100001001110111001100100000011101000110100001100101011100100110010100100000011000010110111001100100001000000110100101110100001001110111001100100000011010010110111000100000011001100110100101101110011001010010000001110011011010000110000101110000011001010010111000100000001000000100011101110010011001010110000101110100001000000111000001110101011110100111101001101100011001010010110000100000011001110111001001100101011000010111010000100000011001100111010101101110001011000010000001100111011100100110010101100001011101000010000001100100011000010111100100100000011101000110111101100100011000010111100100101110"""


def byn(s, n):
    """Convert a string into a list of n-character substrings"""
    out = []
    while s:
        o, s = s[:n], s[n:]
        out.append(o)
    return out


trip = TEXT.split()

# the first 36 non-blank lines are in binary
t36, rest = trip[:36], trip[36:]

# join the lines together into a single string
t1 = "".join(t36)

# split into 8-bit sections
b1 = byn(t1, 8)

# convert from binary text to decimal integer
b2 = map(lambda x: int(x, 2), b1)

# convert to ASCII characters
b3 = [chr(x) for x in b2]

# join together into a string
s1 = "".join(b3)

# and print
print(s1, end=" ")

# get the rest of the characters
r0 = "".join(rest)

# group by two-character pairs
r = byn(r0, 2)

# convert from hex to decimal
rx = map(lambda x: int(x, 16), r)

# convert to characters
cx = [chr(x) for x in rx]

# convert to a string
s2 = "".join(cx)

# and print
print(s2)

# end of file