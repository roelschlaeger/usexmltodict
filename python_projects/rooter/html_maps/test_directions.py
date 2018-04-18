#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
doc string
"""


# import pylint

from html_maps.directions import directions


def test_directions():
    """test the directions() function
    """
    lats = [1, 2]
    lons = [-2, -1]
    start = 0
    end = 1
    waypoints = None
    result = directions(
        lats=lats,
        lons=lons,
        start=start,
        end=end,
        waypoints=waypoints
    )
    print(result)
    assert False
