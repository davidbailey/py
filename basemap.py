from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot
import numpy as np
import CoreLocation

manager = CoreLocation.CLLocationManager.alloc().init()
manager.delegate()
manager.startUpdatingLocation()
loc = manager.location()
if loc is None:
 lat, lon = 0,0
else:
 coord = loc.coordinate()
 lat, lon = coord.latitude, coord.longitude

//def convert_to_decimal(degrees, arcminutes, arcseconds):
// return float(degrees + arcminutes/60. + arcseconds/3600.)

m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

m.drawcoastlines()
m.drawstates()
m.bluemarble()
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
m.drawmapboundary(fill_color='aqua')
m.scatter(lon,lat,100,latlon=1,color='m',marker='.')

pyplot.title("Mercator Projection | Latitude: " + str(lat) + ", Longitude: " + str(lon))
pyplot.show()
