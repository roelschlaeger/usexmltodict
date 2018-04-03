"""
doc string
"""

# import pytest

# from pprint import pprint

from rooter import get_wpts, ellipsis, location_link

DEFAULT_FILENAME = "default.gpx"
DEFAULT_WPTS = 131

########################################################################


def test_location_link():
    """Perform a test of 'location_link' function
    """
    lat = "1.23456"
    lon = "-1.23456"
    retval = location_link(lat, lon)
    expected_value = '<a class="latlon" ' \
        'href="https://www.google.com/search?q=N1%2014.073%20W1%2014.073" ' \
        'target="_blank">(N1 14.073, W1 14.073)</a>'
    assert str(retval) == expected_value


########################################################################


def test_get_wpts():
    """Test the get_wpts function
    """
    gpxname = DEFAULT_FILENAME
    wpts, lat_lon_dictionary = get_wpts(gpxname)

    assert len(wpts) == DEFAULT_WPTS

    wpt = wpts[0]
    assert wpt.keys() == ['lat', 'lon']

    # pprint(lat_lon_dictionary)
    assert lat_lon_dictionary['HOME'] == ('38.798783', '-90.5088')

########################################################################


def test_ellipsis():
    """Test the ellipsis function"""
    expected = [
        (None, None),
        ('', ''),
        ('1', '1'),
        ('12', '12'),
        ('123', '123'),
        ('1234', '1234'),
        ('12345', '12345'),
        ('123456', '123...'),
        ('1234567', '123...'),
        ('12345678', '123...'),
        ('123456789', '123...'),
        ('1234567890', '123...'),
    ]

    length = 6
    for aval, bval in expected:
        result = ellipsis(aval, length)
        print(result, bval)
        assert result == bval


# end of file
