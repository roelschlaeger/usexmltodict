# vim:ts=4:sw=4:tw=0:wm=0:et
# -*- encoding=utf8 -*-


from itertools import compress
import string


def find_message(s):
    return "".join(list(compress(s, [c in string.uppercase for c in s])))

assert find_message("How are you? Eh, ok. Low or Lower? Ohhh.") == "HELLO"
assert find_message("hello world!") == ""
print("Done!")
