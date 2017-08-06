import requests
import pandas
import geopandas
import json
import math
from haversine import haversine
from ipfn import ipfn
import networkx
from matplotlib import pyplot
from matplotlib import patheffects

url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/37/query?where=state%3D06&f=geojson'
r = requests.get(url)
zones = geopandas.GeoDataFrame.from_features(r.json()['features'])
centroidFunction = lambda row: (row['geometry'].centroid.y, row['geometry'].centroid.x)
zones['centroid'] = zones.apply(centroidFunction, axis=1)

url = 'http://api.census.gov/data/2015/acs5/profile?get=NAME,DP03_0018E&for=county&in=state:06'
r = requests.get(url)
Production = pandas.DataFrame(r.json()[1:], columns = r.json()[0], dtype='int')
nameSplit = lambda x: x.split(',')[0]
Production['NAME'] = Production['NAME'].apply(nameSplit)
zones = pandas.merge(zones, Production)
zones['Production'] = zones['DP03_0018E']

def getEmployment(state, county):
  prefix = 'EN'
  seasonal_adjustment = 'U'
  area = format(state, "02d") + format(county, "03d")
  data_type = '1'
  size = '0'
  ownership = '0'
  industry = '10'
  seriesid = prefix + seasonal_adjustment + area + data_type + size + ownership + industry
  headers = {'Content-type': 'application/json'}
  data = json.dumps({"seriesid": [seriesid],"startyear":"2015", "endyear":"2015", "registrationKey": ""})
  p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
  employment = p.json()['Results']['series'][0]['data'][0]['value']
  return(employment)

employment = lambda row: int(getEmployment(row['state'], row['county']))
zones['Attraction'] = zones.transpose().apply(employment)
zones['Production'] = zones['Production'] * zones.sum()['Attraction'] / zones.sum()['Production']
zones.index = zones.NAME
zones.sort_index(inplace=True)

def costFunction(zones, zone1, zone2, beta):
  cost = math.exp(-beta * haversine(zones[zone1]['centroid'], zones[zone2]['centroid']))
  return(cost)

def costMatrixGenerator(zones, costFunction, beta):
  originList = []
  for originZone in zones:
    destinationList = []
    for destinationZone in zones:
        destinationList.append(costFunction(zones, originZone, destinationZone, beta))
    originList.append(destinationList)
  return(pandas.DataFrame(originList, index=zones.columns, columns=zones.columns))

def tripDistribution(tripGeneration, costMatrix):
  costMatrix['ozone'] = costMatrix.columns
  costMatrix = costMatrix.melt(id_vars=['ozone'])
  costMatrix.columns = ['ozone', 'dzone', 'total']
  production = tripGeneration['Production']
  production.index.name = 'ozone'
  attraction = tripGeneration['Attraction']
  attraction.index.name = 'dzone'
  aggregates = [production, attraction]
  dimensions = [['ozone'], ['dzone']]
  IPF = ipfn.ipfn(costMatrix, aggregates, dimensions)
  trips = IPF.iteration()
  return(trips.pivot(index='ozone', columns='dzone', values='total'))

beta = 0.01
costMatrix = costMatrixGenerator(zones.transpose(), costFunction, beta)
trips = tripDistribution(zones, costMatrix)

def modeChoiceFunction(zones, zone1, zone2, modes):
  distance = haversine(zones[zone1]['centroid'], zones[zone2]['centroid'])
  probability = {}
  total = 0.0
  for mode in modes:
    total = total + math.exp(modes[mode] * distance)
  for mode in modes:
    probability[mode] = math.exp(modes[mode] * distance) / total
  return(probability)

def probabilityMatrixGenerator (zones, modeChoiceFunction, modes):
  probabilityMatrix = {}
  for mode in modes:
    originList = []
    for originZone in zones:
      destinationList = []
      for destinationZone in zones:
	  destinationList.append(modeChoiceFunction(zones, originZone, destinationZone, modes)[mode])
      originList.append(destinationList)
    probabilityMatrix[mode] = pandas.DataFrame(originList, index=zones.columns, columns=zones.columns)
  return(probabilityMatrix)

modes = {'walking': .05, 'cycling': .05, 'driving': .05}
probabilityMatrix = probabilityMatrixGenerator(zones.transpose(), modeChoiceFunction, modes)
drivingTrips = trips * probabilityMatrix['driving']

def routeAssignment(zones, trips):
  G = networkx.Graph()
  G.add_nodes_from(zones.columns)
  for zone1 in zones:
    for zone2 in zones:
      if zones[zone1]['geometry'].touches(zones[zone2]['geometry']):
        G.add_edge(zone1, zone2, distance = haversine(zones[zone1]['centroid'], zones[zone2]['centroid']), volume=0.0)
  for origin in trips:
    for destination in trips:
      path = networkx.shortest_path(G, origin, destination)
      for i in range(len(path) - 1):
        G[path[i]][path[i + 1]]['volume'] = G[path[i]][path[i + 1]]['volume'] + trips[zone1][zone2]
  return(G)

def visualize(G, zones):
  fig = pyplot.figure(1, figsize=(10, 10), dpi=90)
  ax = fig.add_subplot(111)
  zonesT = zones.transpose()
  zonesT.plot(ax = ax)
  for i, row in zones.transpose().iterrows():
    text = pyplot.annotate(s=row['NAME'], xy=((row['centroid'][1], row['centroid'][0])), horizontalalignment='center', fontsize=6)
    text.set_path_effects([patheffects.Stroke(linewidth=3, foreground='white'), patheffects.Normal()])
  for zone1 in G.edge:
    for zone2 in G.edge[zone1]:
      volume = G.edge[zone1][zone2]['volume']
      x = [zones[zone1]['centroid'][1], zones[zone2]['centroid'][1]]
      y = [zones[zone1]['centroid'][0], zones[zone2]['centroid'][0]]
      ax.plot(x, y, color='#444444', linewidth=volume/10000, solid_capstyle='round', zorder=1)
  pyplot.show(block=False)

G = routeAssignment(zones.transpose(), drivingTrips)
visualize(G, zones.transpose())
