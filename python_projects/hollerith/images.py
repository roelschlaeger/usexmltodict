#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 03 May 2016 03:25:54 PM CDT
# Last Modified: Tue 03 May 2016 04:09:51 PM CDT

from read_image import read_image, STARTX, STARTY, ENDX, ENDY
from read_image import HOLLERITH_COLUMNS, HOLLERITH_ROWS
from read_image import LATITUDE_IMAGE, LONGITUDE_IMAGE, MY_LATITUDE_IMAGE
from im2holl import image_to_hollerith, hollerith_to_strings
from beginning import decode_strings


class Image(object):

    def __init__(
        self,
        imagename,
        start_x=STARTX,
        start_y=STARTY,
        end_x=ENDX,
        end_y=ENDY
    ):
        self.imagename = imagename
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y
        self.pitch_x = (self.end_x - self.start_x) / float(HOLLERITH_COLUMNS - 1)
        self.pitch_y = (self.end_y - self.start_y) / float(HOLLERITH_ROWS - 1)
        self.data = None
        self.hollerith = None
        self.strings = None
        self.decode = None

    def read(self):
        self.data = read_image(
            self.imagename,
            start_x=self.start_x,
            pitch_x=self.pitch_x,
            start_y=self.start_y,
            pitch_y=self.pitch_y
        )

    def to_hollerith(self):
        self.hollerith = image_to_hollerith(self.data)

    def to_strings(self):
        self.strings = \
            "\n" + \
            "\n".join(hollerith_to_strings(self.hollerith)) + \
            "\n"

    def to_decode(self):
        self.decode = decode_strings(self.strings)

    def process(self):
        self.read()
        self.to_hollerith()
        self.to_strings()
        self.to_decode()


im1 = Image(LATITUDE_IMAGE, 27.5, 25, 609, 265)
im2 = Image(LONGITUDE_IMAGE, 27, 27, 609, 267)
im3 = Image(MY_LATITUDE_IMAGE, 27, 26, 738, 320)

im1.process()
print(im1.decode)

# im2.process()
# print(im2.decode)

# im3.process()
# print(im3.decode)
