# -*- coding utf-8 -*-
"""
Create a collection of <wpt> Elements.

Copyright (c) 2016 Robert Oelschlaeger All Rights Reserved
roelsch2009@gmail.com
"""

from __future__ import print_function
from xml.etree import ElementTree as ET

#######################################################################


def get_wpts(root):
    """Return a collection of <wpt> Elements from <root>."""
    wpt_tag = root.tag.replace("gpx", "wpt")
    wpts = root.findall(wpt_tag)
    return wpts

#######################################################################


def print_children(w0):
    """Print the children nodes of the w0 Element."""
    pprint(w0.getchildren())
    for item in w0.getchildren():
        print("'%s' : '%s'" % (item.tag.split("}")[1], item.text))

#######################################################################


def name_desc_dict(wpts):
    """Return a dictionary of (name, desc) pairs from wpts."""
    wpt_tag = wpts[0].tag
    name_tag = wpt_tag.replace("wpt", "name")
    desc_tag = wpt_tag.replace("wpt", "desc")
    names = dict(
        (
            wpt.find(name_tag).text,
            wpt.find(desc_tag).text
        ) for wpt in wpts
    )

    return names

#######################################################################

if __name__ == "__main__":

    INFILE = "default.gpx"

    from pprint import pprint

    tree = ET.parse(INFILE)
    root = tree.getroot()
    wpts = get_wpts(root)

    w0 = wpts[0]
    print_children(w0)

    names = name_desc_dict(wpts)
    # pprint(names)
