import pandas
import numpy
import gtfstk
from shapely.geometry import Point
import matplotlib.pyplot as plt
from datetime import timedelta
from os.path import expanduser
import geopandas

amtrak = gtfstk.feed.Feed(expanduser('~/Desktop/amtrak_20140723_0354.zip')) #http://www.gtfs-data-exchange.com/agency/amtrak/
trip_ids = amtrak.trips[(amtrak.trips['route_id'] == '66') & (amtrak.trips['direction_id'] == 0)]['trip_id']
stops = pandas.merge(pandas.DataFrame(trip_ids),amtrak.stop_times)
trains = stops.groupby('trip_id')

def combine(listA,listB):
  if not listA:
    return listB
  elif not listB:
    return listA
  elif listA[0] == listB[0]:
    newList = [listA[0]]
    newList.extend(combine(listA[1:],listB[1:]))
    return newList
  elif listA[0] in listB:
    return combine(listB,listA)
  else:
    newList = [listA[0]]
    newList.extend(combine(listA[1:],listB))
    return newList

stop_ids = []
for index, train in trains:
  train = train.sort('stop_sequence')
  stop_ids = combine(stop_ids,list(train['stop_id']))

previousStop = False
distances = []
stopLocations = []
midPoints = []
for stop in stop_ids:
  if previousStop:
    currentStop = Point(float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lat']),float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lon']))
    distanceToPreviousStop = 65.93*currentStop.distance(previousStop)
    distances.append(distanceToPreviousStop)
    midPoints.append(Point((previousStop.x+currentStop.x)/2,(previousStop.y+currentStop.y)/2))
  previousStop = Point(float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lon']),float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lat']))
  stopLocations.append(previousStop)

times = []
for index, train in trains:
  #time = [list(train['trip_id'])[0]]
  time = []
  departureTime = False
  for stop in stop_ids:
    if stop in list(train['stop_id']):
      if departureTime:
        h, m, s = map(int,list(train[train['stop_id'] == stop]['arrival_time'])[0].split(':'))
        arrivalTime = timedelta(hours=h, minutes=m, seconds=s)
        delta = arrivalTime - departureTime
        time.append(delta.total_seconds()/60/60)
      h, m, s = map(int,list(train[train['stop_id'] == stop]['departure_time'])[0].split(':'))
      departureTime = timedelta(hours=h, minutes=m, seconds=s)
    else:
      time.append(0)
  times.append(time)

stopsGDF = geopandas.GeoDataFrame(stopLocations,stop_ids)
stopsGDF.columns = ['geometry']

stop_ids.pop()
distancesS = pandas.Series(distances)
timesDF = pandas.DataFrame(times)
speedDF = distancesS / timesDF
speedDF.columns = stop_ids
speedDFT = speedDF.transpose()

speedDFT.plot(legend=False)
ax = plt.axes()
ax.yaxis.grid()
plt.show()

speedDF = distancesS / timesDF
speedGDF = geopandas.GeoDataFrame(speedDF)
speedGDFT = speedGDF.transpose()
speedGDFT['geometry'] = midPoints

stopsGDF.to_json()
speedGDFT.to_json()
