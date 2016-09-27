# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/three-words/


def category(s):
    letters = all([c.isalpha() for c in s])
    return "a" if letters else "-"


def checkio(s):
    words = s.split()
    categories = [category(word) for word in words]
    return "".join(categories).find("aaa") != -1

assert checkio("Hello World hello") == True
assert checkio("He is 123 man") == False
assert checkio("1 2 3 4") == False
assert checkio("bla bla bla bla") == True
assert checkio("Hi") == False
print("Done!")
