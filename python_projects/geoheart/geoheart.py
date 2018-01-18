#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 15 Feb 2017 08:55:30 AM CST
# Last Modified: Wed 15 Feb 2017 12:14:55 PM CST

# parse Geo(he)art caches

###############################################################################

"""Collect FINAL cache locations from Geo(he)Art cache descriptions."""

###############################################################################

from __future__ import print_function

from geoheart_data import data
from geoheart_data import TEXT1, TEXT2
from pprint import pformat
import re
import urllib2

###############################################################################

OUTFILE = "geoheart.csv"

###############################################################################


def main():
    """Collect FINAL cache locations from Geo(he)Art cache descriptions."""
    with open(OUTFILE, "wt") as outfile:

        print(
            "\t".join(
                [
                    "Code",
                    "Description",
                    "URL",
                    "Rosetta",
                    "Maurelle"
                ]
            ),
            file=outfile
        )

        for gc_code, gc_name, gc_url in data[6:7]:

            # start with default result
            result = {
                "Rosetta": "",
                "Maurelle": ""
            }

            print(gc_code, gc_name, gc_url)

            response = urllib2.urlopen(gc_url)
            html = response.read()

            for text in [TEXT1, TEXT2]:

                expression = re.compile(text)

                m = expression.search(html)
                if m is not None:
                    print(pformat(m.group(0)))
                    name = m.group(1)
                    lat = m.group(2)
                    lon = m.group(3)
                    print("name = '%s'" % name)
                    print("lat = '%s'" % lat)
                    print("lon = '%s'" % lon)
                    result[name] = '%s %s' % (lat, lon)
                else:
                    print("No match for %s in %s" % (text, gc_url))

            print(
                "%s\t%s\t%s\t%s\t%s" % (
                    gc_code,
                    gc_name,
                    gc_url,
                    result["Rosetta"],
                    result["Maurelle"]
                ),
                file=outfile
            )

    print("\nResults are in %s\n" % OUTFILE)


if __name__ == "__main__":

    main()

# end of file
