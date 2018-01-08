# taken from https://github.com/vgm64/gmplot

from with_sqlite3 import get_data
import gmplot

FILENAME = "output_file.db"
FIVEHUNDREDFEET = 152.4  # 500 feet converted to meters

# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)

data = get_data(FILENAME)
latitudes, longitudes, texts, syms = list(zip(*data))[:4]
# latitudes = [d[0] for d in data]
# longitudes = [d[1] for d in data]
# texts = [d[2] for d in data]
# syms = [d[3] for d in data]

# compute centerpoint
if 0:
    # center on map center
    clat = (max(latitudes) + min(latitudes)) / 2.
    clon = (max(longitudes) + min(longitudes)) / 2.
    zoom = 10
else:
    # center on starting point
    clat = latitudes[0]
    clon = longitudes[0]
    zoom = 18
gmap = gmplot.GoogleMapPlotter(clat, clon, zoom)
gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=6)
# gmap.scatter(
#     latitudes, longitudes, '#ff0000', size=FIVEHUNDREDFEET, marker=False
# )
gmap.scatter(latitudes, longitudes, 'k', marker=True)
# gmap.heatmap(latitudes, longitudes)

gmap.draw("mymap.html")
print("Output is in 'mymap.html'")

# end of file
