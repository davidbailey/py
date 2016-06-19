import gpxpy
from os.path import expanduser
from math import sqrt
from shapely.geometry import Point
import geopandas
import numpy
from matplotlib import pyplot

with open(expanduser('~/Desktop/2016-06-14 19_13_54.gpx'), 'r') as gpx_file:
  gpx = gpxpy.parse(gpx_file)

gpx.tracks[0].segments[0].points[0].time
gpx.tracks[0].segments[0].points[0].latitude
gpx.tracks[0].segments[0].points[0].longitude

speeds = []
for i in range(0, len(gpx.tracks[0].segments[0].points) - 1):
  deltaLatitude = gpx.tracks[0].segments[0].points[i].latitude - gpx.tracks[0].segments[0].points[i - 1].latitude
  deltaLongitude = gpx.tracks[0].segments[0].points[i].longitude - gpx.tracks[0].segments[0].points[i - 1].longitude
  speed = sqrt(deltaLatitude**2 + deltaLongitude**2) * 69.04799998422561 * 3600 # not sure if this is the right conversion
  midLatitude = (gpx.tracks[0].segments[0].points[i].latitude + gpx.tracks[0].segments[0].points[i - 1].latitude) / 2 
  midLongitude = (gpx.tracks[0].segments[0].points[i].longitude + gpx.tracks[0].segments[0].points[i - 1].longitude) /2
  speeds.append((Point(midLongitude, midLatitude), midLatitude, midLongitude, speed))

speedsDF = geopandas.GeoDataFrame(speeds, columns=('geometry', 'latitude', 'longitude', 'speed'))

# from http://stackoverflow.com/questions/25526682/functions-to-smooth-a-time-series-with-known-dips
filtered = speedsDF.speed.copy()
dm = speedsDF.speed.rolling(window=20,center=True).median()
df = sorted(numpy.abs(speedsDF.speed - dm).dropna(), reverse=True)
cutoff = df[len(df) // 20] 
filtered[numpy.abs(speedsDF.speed - dm) > cutoff] = numpy.nan
filtered[0] = numpy.nan
speedsDF['filtered'] = filtered
speedsDF.dropna(subset=['filtered'], inplace=True)

f, ax = pyplot.subplots(2, sharex=True)
speedsDF.plot(ax=ax[0], column='filtered', cmap='OrRd', markersize=10, marker='.')
ax[1].plot(speedsDF.longitude, speedsDF.filtered)
pyplot.show()
