# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/rotate-hole/


def rotate(rotary, cannons):

    out = []
    for i in range(len(rotary)):
        for c in cannons:
            if not rotary[c]:
                break
        else:
            out.append(i)

        rotary.insert(0, rotary.pop())
    return out


assert rotate([1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1]) == [1, 8]
assert rotate([1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 2]) == []
assert rotate([1, 0, 0, 0, 1, 1, 0, 1], [0, 4, 5]) == [0]
assert rotate([1, 0, 0, 0, 1, 1, 0, 1], [5, 4, 5]) == [0, 5]
print("Done!")
