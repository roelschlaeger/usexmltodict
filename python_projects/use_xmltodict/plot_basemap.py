"""Plot waypoints on geo basemap"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from math import ceil, floor

########################################################################


def plot_waypoints(data):
    """Plot waypoints on a basemap.

    data consists of:

        (latitude, longitude, text, sym) tuples

    where only latitude and longitude are relevant to plotting so far.
"""

    # extract lists of latitudes and longitudes
    latitudes, longitudes = list(zip(*data))[:2]

    # compute min and max
    minlat = floor(min(latitudes))
    maxlat = ceil(max(latitudes))

    # compute min and max
    minlon = floor(min(longitudes))
    maxlon = ceil(max(longitudes))

#   texts = [d[2] for d in data]
#   syms = [d[3] for d in data]

    m = Basemap(
        projection='mill',
        llcrnrlat=minlat,
        urcrnrlat=maxlat,
        llcrnrlon=minlon,
        urcrnrlon=maxlon,
        resolution='i'
    )
    m.drawparallels(range(minlat, maxlat), labels=[1, 0, 0, 1])
    m.drawmeridians(range(minlon, maxlon), labels=[0, 1, 0, 1])
    m.drawcoastlines()
    m.fillcontinents(color='#04BAE340', lake_color='#FFFFFF')
    m.drawcountries()
    m.drawstates()
    m.drawcounties()
    m.drawmapboundary(fill_color='#FFFFFF')

    for lat, lon in zip(latitudes, longitudes):
        x, y = m(lon, lat)
        m.plot(x, y, 'go')

    plt.title("Geo Plotting")
    plt.show()


########################################################################

if __name__ == "__main__":

    from with_sqlite3 import get_data
    FILENAME = "output_file.db"

    plot_waypoints(get_data(FILENAME))

# end of file
