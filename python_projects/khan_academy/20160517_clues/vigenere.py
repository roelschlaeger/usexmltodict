# coding=utf-8

"""Perform Viginere decoding for a ciphertext from Khan Academy."""

from __future__ import print_function

########################################################################

CIPHERTEXT = """
KLKBNQLCYTFYSRYUCOCPHGBDIZZFCMJWKUCHZYESWFOGMMETWWOSSDCHRZYLDSBWNYDEDN
ZWNEFYDTHTDDBOJICEMLUCDYGICCZHOADRZCYLWADSXPILPIECSKOMOLTEJTKMQQYMEHPM
MJXYOLWPEEWJCKZNPCCPSVSXAUYODHALMRIOCWPELWBCNIYFXMWJCEMCYRAZDQLSOMDBFL
JWNBIJXPDDSYOEHXPCESWTOXWBLEECSAXCNUETZYWFN
"""

ciphertext = CIPHERTEXT.replace("\n", "")

########################################################################


def viginere(s, key):
    """Decode the string s with a key."""
    # create a generator that cyclically repeats the key characters
    def keygen(key):
        while 1:
            for c in key:
                yield c

    #   # set up to encode
    #   def encode(c1, c2):
    #       n1 = ord(c1) - ord('A')
    #       n2 = ord(c2) - ord('A')
    #       return chr(((n1 + n2) % 26) + ord('A'))

    # set up to decode
    def decode(c1, c2):
        n1 = ord(c1) - ord('A')
        n2 = ord(c2) - ord('A')
        return chr(((n1 - n2) % 26) + ord('A'))

    # prepare the empty output list
    out = []

    # create the cyclic key generator
    gen = keygen(key.upper())

    # decode each of the characters
    for c in s.upper():
        out.append(decode(c, gen.next()))

    # return the result string
    return "".join(out)

########################################################################

if __name__ == '__main__':

    def main():
        """Perform processing from the command line."""
        print("Ciphertext")
        print(ciphertext)
        print(viginere(ciphertext, key="SSKKUULLLL"))
        print()

        print("Ciphertext2")
        ciphertext2 = """
RYSMYSDIXRYKPQPRHVOBDSGUXAYPYPRPQRHVOXQYHPMOSFVNXMOMEQCXQSRYMXQC
VMGPLHVMKXMKAYAMVIVRRSCVRPYPRRAMVDZAQBMVSUSBDVPYGXIBPQVRXAMLMVEWXARIVYH
MLQQVNR
""".replace("\n", "")
        print(ciphertext2)
        print(viginere(ciphertext2, key="SSKKUULLLL"))
        print()

    main()

# end of file
