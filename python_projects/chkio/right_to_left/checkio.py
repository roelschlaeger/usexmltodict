# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-

# https://py.checkio.org/mission/right-to-left/


def left_join(t):
    out = []
    for w in t:
        out.append(
            w
            .replace("right", "left")
        )
    return ",".join(out)

assert left_join(("left", "right", "left", "stop")) == "left,left,left,stop"
assert left_join(("bright aright", "ok")) == "bleft aleft,ok"
assert left_join(("brightness wright",)) == "bleftness wleft"
assert left_join(("enough", "jokes")) == "enough,jokes"
print("Done!")

# end of file
