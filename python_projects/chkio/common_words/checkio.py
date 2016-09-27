# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/common-words/


def checkio(s1, s2):
    w1 = set(s1.split(","))
    w2 = set(s2.split(","))
    return ",".join(sorted(w1.intersection(w2)))

assert checkio("hello,world", "hello,earth") == "hello"
assert checkio("one,two,three", "four,five,six") == ""
assert checkio("one,two,three", "four,five,one,two,six,three") == "one,three,two"
print("Done!")

