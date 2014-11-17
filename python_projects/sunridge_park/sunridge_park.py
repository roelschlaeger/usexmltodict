from geopy import Point
import simplekml


SAVEFILENAME = "sunridge_park.kml"


def main():
#   The final is at N38 19.7XX W090 31.8XX
# To get the last two of the north coordinates take (Planks x 7) + 1
# To get the last two of the west coordinates take (windows x 4) + 1

    kml = simplekml.Kml()
    coordinates = []

    for planks in range(14+1):
        for windows in range(24+1):
            lat = "38 19.7%02dm 0s N" % (planks * 7 + 1)
            lon = "90 31.8%02dm 0s W" % (windows * 4 + 1)
            point = Point.from_string("%s;%s" % (lat, lon))
            name = "L_p%02d_w%02d" % (planks, windows)

            coordinate = (name, point)
            coordinates.append(coordinate)
            coords = [(point.longitude, point.latitude)]
            kml.newpoint(name=name, coords=coords)

    kml.save(SAVEFILENAME)
    print "Output is in %s" % SAVEFILENAME

if __name__ == "__main__":
    main()
