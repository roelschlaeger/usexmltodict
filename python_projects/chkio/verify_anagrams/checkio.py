# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/verify-anagrams/

from collections import Counter


def verify_anagrams(s1, s2):
    return Counter(s1.lower().replace(" ", "")) == Counter(s2.lower().replace(" ", ""))


assert verify_anagrams("Programming", "Gram Ring Mop") == True
assert verify_anagrams("Hello", "Ole Oh") == False
assert verify_anagrams("Kyoto", "Tokyo") == True
print("Done!")
# end of file
