#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 15 Feb 2017 08:55:30 AM CST
# Last Modified: Wed 15 Feb 2017 08:56:56 AM CST

# parse Geo(he)art caches

from __future__ import print_function
import urllib2
from HTMLParser import HTMLParser
from geoheart_data import data


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

for code, name, url in data:
    print(code, name, url)
    response = urllib2.urlopen(url)
    html = response.read()
    parser.feed(html)
    break

# end of file
