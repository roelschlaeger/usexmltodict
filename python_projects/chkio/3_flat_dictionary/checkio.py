# vim:ts=4:sw=4:tw=0:wm=0:et

# https://py.checkio.org/mission/flatten-dict/

"""Flatten a dictionary for Sophie"""

########################################################################


def flatten(s):
    """Flatten a dictionary"""
    # print "Flatten %s" % s
    o = {}
    for k, v in s.iteritems():

        if v == {}:
            v = ""

        # check for recursion
        if isinstance(v, dict):
            d2 = flatten(v)
            for k2, v2 in d2.iteritems():
                newkey = "%s/%s" % (k, k2)
                o[newkey] = v2
        else:
            o[k] = v

    return o

########################################################################

# s = {
#     "name": {"first": "One", "last": "Drone"},
#     "job": "scout",
#     "recent": {},
#     "additional": {"place": {"zone": "1", "cell": "2"}}
# }

# from pprint import pprint
# pprint(s)
# print 72 * '#'
# pprint(flatten(s))

########################################################################

assert flatten({"key": "value"}) == {"key": "value"}
assert flatten({"key": {"deeper": {"more": {"enough": "value"}}}}) == {"key/deeper/more/enough": "value"}
assert flatten({"empty": {}}) == {"empty": ""}
