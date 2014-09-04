#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 04 Sep 2014 03:58:56 PM CDT
# Last Modified: Thu 04 Sep 2014 04:41:58 PM CDT

__VERSION__ = "0.0.1"

########################################################################

from collections import defaultdict, OrderedDict
# from pprint import pprint

if 1:

    CACHE_DATA = OrderedDict()

    for line in (open("cache_data.txt")).readlines()[1:]:
        key, value = line.split("\t")
        CACHE_DATA[key] = value[:-1]

#   pprint(CACHE_DATA)

else:
    from found_dict import CACHE_DATA

########################################################################


def show_all(CACHE_DATA):
    for key in sorted(dictionary.keys()):
        print key
        for key2, cache in dictionary[key].items():
            print "\t", key2, cache
        print

########################################################################


def show_first_last(CACHE_DATA):
    for key in sorted(dictionary.keys()):
        l = dictionary[key].items()
        print key, len(l)
        first = l[0]
        last = l[-1]
        print "\t", first[:]
        print "\t", last[:]
        print

########################################################################


def show_first(CACHE_DATA):
    for key in sorted(dictionary.keys()):
        l = dictionary[key].items()
        first = l[0]
        print key, first[:]

    print

########################################################################


def show_last(CACHE_DATA):
    for key in sorted(dictionary.keys()):
        l = dictionary[key].items()
        last = l[-1]
        print key, last[:]

    print

########################################################################


def separator():
    print
    print 80 * '#'
    print

########################################################################

dictionary = defaultdict(OrderedDict)

for key, value in CACHE_DATA.items():
    index = key[2]
    d = dictionary[index]
    d[key] = value

# show_all(CACHE_DATA)
# separator()
# show_first_last(CACHE_DATA)
# separator()
show_first(CACHE_DATA)
separator()
show_last(CACHE_DATA)

# end of file
