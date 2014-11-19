# vim:ts=4:sw=4:tw=0:wm=0
# -*- encoding:utf-8 -*-

from geopy import Point
import simplekml
from geopy.distance import great_circle


# Rainman indicated that the cache is within about 30' of the base of the tower.
#
# I've got the tower location eyeballed to be:
#
# TOWER_LOCATION = "N38° 19.773'  W90° 31.868'"
tower_location = (38. + 19.773 / 60., -(90. + 31.868 / 60.))

SAVEFILENAME = "sunridge_park.kml"


def main():
#   The final is at N38 19.7XX W090 31.8XX
# To get the last two of the north coordinates take (Planks x 7) + 1
# To get the last two of the west coordinates take (windows x 4) + 1

    kml = simplekml.Kml()

    # the list of candidate location
    coordinates = []

    for planks in range(14 + 1):

#       from the photo of the tower on Flikr it is apparent that there are 16
#       windows:

#       for windows in range(24 + 1):
        for windows in [16]:

            # compute the cache location
            lat = "38 19.7%02dm 0s N" % (planks * 7 + 1)
            lon = "90 31.8%02dm 0s W" % (windows * 4 + 1)
            point = Point.from_string("%s;%s" % (lat, lon))

            # generate a name
            name = "L_p%02d_w%02d" % (planks, windows)

            # compute a distance, in feet, from the tower
            distance = great_circle(
                tower_location,
                (
                    point.latitude,
                    point.longitude
                )
            ).feet

            # only keep the nearby results
            if distance < 100:

                #
                coordinate = (name, point)

                # add the candidate to the list
                coordinates.append(coordinate)

                # display the points as a KML file
                coords = [(point.longitude, point.latitude)]
                kml.newpoint(name=name, coords=coords)

                # show the locations to the console
                print name, distance, str(point)

    # output the KML file
    kml.save(SAVEFILENAME)

    # keep the user informed
    print "Output is in %s" % SAVEFILENAME

if __name__ == "__main__":
    main()
