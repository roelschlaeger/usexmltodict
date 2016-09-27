# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/absolute-sorting/


def checkio(t):
    return sorted(list(t), key=abs)

assert checkio((-20, -5, 10, 15)) == [-5, 10, 15, -20]  # or (-5, 10, 15, -20)
assert checkio((1, 2, 3, 0)) == [0, 1, 2, 3]
assert checkio((-1, -2, -3, 0)) == [0, -1, -2, -3]
print("Done!")


