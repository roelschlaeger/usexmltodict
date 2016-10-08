# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/vigenere-cipher/

from __future__ import print_function

########################################################################

ORDA = ord('A')
DEBUG = True

########################################################################


def keygen(p, c):
    """Recover a key from plaintext 'p' and ciphertext 'c'."""
    s = "".join([key_delta(x, y) for (x, y) in zip(p, c)])
    if DEBUG:
        print("keygen", s, len(s))

    pos = len(s)
    for loc in range(1, len(s)):
        if s[:loc] == s[loc:loc * 2]:
            if DEBUG:
                print("keygen", loc)
            pos = loc

    if DEBUG:
        print()
    key = s[:pos]
    last = (len(s) // pos) * pos
    if DEBUG:
        print("last", last)
    if not key.startswith(s[last:]):
        key = s
    if DEBUG:
        print("key", key)
    return key

########################################################################


def key_delta(p, c):
    """Compute the key character that was added to 'p' to yield 'c'."""
    oc = ord(c) - ORDA
    op = ord(p) - ORDA
    d = oc - op
    if d < 0:
        d += 26
    return chr(d + ORDA)

########################################################################


def encode(p, k):

    from itertools import cycle

    # repeatedly use the key characters
    g = cycle(k)

    out = []
    for c in p:
        k = g.next()
        d = ord(c) - ord(k)
        if d < 0:
            d += 26
        out.append(chr(ORDA + d))
    return "".join(out)

########################################################################


def decode_vigenere(plaintext, ciphertext, newciphertext):

    key = keygen(plaintext, ciphertext)
    result = encode(newciphertext, key)
    if DEBUG:
        print("result", result, "\n")
    return result

########################################################################

if __name__ == "__main__":

    assert decode_vigenere('HELLO', 'OIWWC', 'ICP') == "BYE"
    assert decode_vigenere(
        u"DONTWORRYBEHAPPY",
        u"FVRVGWFTFFGRIDRF",
        u"DLLCZXMFVRVGWFTF"
    ) == u"BEHAPPYDONTWORRY"
    assert decode_vigenere(
        u"ANDNOWFORSOMETHINGCOMPLETELYDIFFERENT",
        u"PLWUCJUMKZCZTRAPBTRMFWZRICEFRVUDXYSAI",
        u"XKTSIZQCKQOPZYGKWZDIBZZRTNTSZAXEAAOASGPVFXPJEKOLXANARBLLMYSRHGLRWCPLWQIZEGEPYRIMIYSFHUBSRSAMPLFFXNNACALMFLBFRJHAVVCETURUPLZHFBJLWPBOPPL") == \
        u"IMALUMBERJACKANDIMOKISLEEPALLNIGHTANDIWORKALLDAYICUTDOWNTREESISKIPANDJUMPILIKETOPRESSWILDFLOWERSIPUTONWOMENSCLOTHINGANDHANGAROUNDINBARS"
    assert decode_vigenere(
        u"NOBODYEXPECTSTHESPANISHINQUISITION",
        u"PVFQNGSZWIEDAHJLWRKVWUOMPACWUPXKYV",
        u"QBVGHXSTAWFOAQTPFGIWICZEPKXDCSPKXOZAKYNVNSNSSYEVWOHKKXIHKCIVSUWFSEEUQBIPRKXQHKHXKFMGRPRGVMGULEUSTMFVQKXIHGKRQCMBULSHRCAQBVVOLWQBWEYUDCUCCXLWTYIRBMGUPFNILFCIEPNIKHBPCXLKJLVGKAWPTSUDXFQMIUCQCPZXJOASYVYNNJSEVRUSLSTHFNOLFCDFCMSGKUGJKZHGYIFKKQQBRVKVQAALGIIFGHTQCQHKCIDYWB") == \
        u"OUREXPERTSDESCRIBEYOUASANAPPALLINGLYDULLFELLOWUNIMAGINATIVETIMIDLACKINGININITIATIVESPINELESSEASILYDOMINATEDNOSENSEOFHUMOURTEDIOUSCOMPANYANDIRREPRESSIBLYDRABANDAWFULANDWHEREASINMOSTPROFESSIONSTHESEWOULDBECONSIDERABLEDRAWBACKSINCHARTEREDACCOUNTANCYTHEYAREAPOSITIVEBOON"
    assert decode_vigenere(
        u"AAAAAAAAAAAAAA",
        u"ABABABABABABAC",
        u"WIAUITGPIOGPNJESE") == "WHATISGOINGONHERE"
# end of file
