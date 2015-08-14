import overpy
import numpy
from matplotlib import pyplot
from shapely.geometry import LineString
from shapely.geometry import shape
from shapely.geometry import box
from shapely.ops import polygonize_full
from descartes import PolygonPatch
from fiona import collection

features = collection("~/Desktop/gshhg-shp-2/GSHHS_shp/f/GSHHS_f_L1.shp")
northAmericaPolygon = shape(features[3]['geometry'])

laBox = box(-119.3500,33.5277,-117.1115,34.9895)
coastBox = northAmericaPolygon.intersection(laBox)

api = overpy.Overpass()

countyRelation = api.query("rel(396479);(._;>;);out;")
primaryHighwaysInBoundingBox = api.query("way(33.5277,-119.3500,34.9895,-117.1115)[highway=primary];(._;>);out;")
secondaryHighwaysInBoundingBox = api.query("way(33.5277,-119.3500,34.9895,-117.1115)[highway=secondary];(._;>);out;")

countyWaysAboveIslands = []
for way in countyRelation.ways:
 above = 1
 for node in way.nodes:
  if (node.lat < 33.6078):
   above = 0
 if (above):
  countyWaysAboveIslands.append(way)

countyLineStrings = []
for way in countyWaysAboveIslands:
 lineString = []
 for node in way.nodes:
  lineString.append((node.lon,node.lat))
 countyLineStrings.append(LineString(lineString))

polygons, dangles, cuts, invalids = polygonize_full(countyLineStrings)
countyPolygonWithOcean = polygons.geoms[0]

countyPolygon = countyPolygonWithOcean.intersection(coastBox)

highwayLineStrings = []
for way in primaryHighwaysInBoundingBox.ways:
 line = []
 for node in way.nodes:
  line.append((node.lon,node.lat))
 wayLineString = LineString(line)
 if countyPolygon.contains(wayLineString): highwayLineStrings.append(wayLineString)

for way in secondaryHighwaysInBoundingBox.ways:
 line = []
 for node in way.nodes:
  line.append((node.lon,node.lat))
 wayLineString = LineString(line)
 if countyPolygon.contains(wayLineString): highwayLineStrings.append(wayLineString)

fig = pyplot.figure(figsize=(100,100))
ax = fig.add_subplot(111)

for line in highwayLineStrings:
 x, y = line.xy
 ax.plot(x, y, color='#FFFFFF', linewidth=1, zorder=2)

patch = PolygonPatch(countyPolygon, fc='#FFD700', ec='#FFD700', alpha=0.5, zorder=1)
ax.add_patch(patch)

fig.savefig('test2.png')

## Pickle
>>> import pickle
>>> output = open('data.pkl', 'wb')
>>> pickle.dump(countyPolygon,output)
>>> pickle.dump(highwayLineStrings,output)
>>> output.close()

## debug info
from geopandas import GeoSeries
from geopandas import GeoDataFrame

from shapely.geometry import MultiLineString
test = MultiLineString(highwayLineStrings)
patch = PolygonPatch(countyPolygon, fc='#6699cc', ec='#6699cc', alpha=0.5, zorder=2)
ax.add_patch(patch)

object.__dict__
result.nodes
result.nodes.[0].lat
result.ways
result.ways[0]._node_ids[0]
result.relations
result.relations[0].members[0].ref

len(streetsInBB.ways[0].get_nodes(resolve_missing=True))

for way in aboveIslands:
 gray = gray + .025
 for node in way.nodes:
  ax.scatter(node.lon, node.lat, color=[gray,gray,gray], s=100, zorder=1)

states = [shapely.geometry.shape(f['geometry']) for f in features]

http://overpass.osm.rambler.ru/cgi/interpreter?data=%5Bout:json%5D;relation(396479);out;
