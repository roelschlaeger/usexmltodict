# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/bird-language/

from __future__ import print_function

"""Translate from bird language to English"""

vowel = "aeiouy"

consonant = "bcdfghjklmnpqrstvwxz"


def generator(s):
    """Define a generator for the string s."""
    for c in s:
        yield c


def translate(s):
    """Translate 's' from bird language to English."""
    g = generator(s.lower())
    out = []

    while 1:
        try:
            c = g.next()
            out.append(c)
            if c in consonant:
                g.next()
            elif c in vowel:
                g.next()
                g.next()
            else:
                pass
        except StopIteration:
            break
    result = "".join(out)
    print(result)
    return result

assert translate("hieeelalaooo") == "hello"
assert translate("hoooowe yyyooouuu duoooiiine") == "how you doin"
assert translate("aaa bo cy da eee fe") == "a b c d e f"
assert translate("sooooso aaaaaaaaa") == "sos aaa"
print("Done!")
