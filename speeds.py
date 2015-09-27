import pandas
import numpy
import gtfstk
from shapely.geometry import Point
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from datetime import timedelta
from os.path import expanduser
import geopandas
from bottle import route, run, template

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

def getJSONs(route,direction):
  amtrak = gtfstk.feed.Feed(expanduser('~/Desktop/amtrak_20140723_0354.zip')) #http://www.gtfs-data-exchange.com/agency/amtrak/
  trip_ids = amtrak.trips[(amtrak.trips['route_id'] == str(route)) & (amtrak.trips['direction_id'] == int(direction))]['trip_id']
  stops = pandas.merge(pandas.DataFrame(trip_ids),amtrak.stop_times)
  trains = stops.groupby('trip_id')
  stop_ids = []
  for index, train in trains:
    train = train.sort('stop_sequence')
    stop_ids = combine(stop_ids,list(train['stop_id']))
  previousStop = False
  distances = []
  stopLocations = []
  lineStrings = []
  for stop in stop_ids:
    if previousStop:
      currentStop = Point(float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lon']),float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lat']))
      distanceToPreviousStop = 65.93*currentStop.distance(previousStop)
      distances.append(distanceToPreviousStop)
      lineStrings.append(LineString([list(currentStop.coords)[0],list(previousStop.coords)[0]]))
    previousStop = Point(float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lon']),float(amtrak.stops[amtrak.stops['stop_id'] == stop]['stop_lat']))
    stopLocations.append(previousStop)
  times = []
  for index, train in trains:
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
  distancesS = pandas.Series(distances)
  timesDF = pandas.DataFrame(times)
  timesDF = timesDF.replace(0.0, numpy.nan)
  speedS = distancesS / timesDF.mean()
  speedS = speedS.round(2)
  speedGDF = geopandas.GeoDataFrame(lineStrings,speedS)
  speedGDF.columns = ['geometry']
  return [stopsGDF.to_json(), speedGDF.to_json()]

@route('/<route>/<direction>')
def index(route,direction):
  stops, speeds = getJSONs(route,direction)
  f = open(expanduser('~/Desktop/speeds.tpl'), 'r')
  return template(f.read(), speeds = speeds, stops = stops)
  f.close()

run(host='localhost', port=8080)

#speedDFlables = stop_ids
#speedDFlables.pop()
#speedDF = distancesS / timesDF
#speedDF.columns = speedDFlables 
#speedDFT = speedDF.transpose()

#speedDFT.plot(legend=False)
#ax = plt.axes()
#ax.yaxis.grid()
#plt.show()
