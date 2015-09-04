import overpy
import numpy
import pickle
from matplotlib import pyplot
from shapely.geometry import LineString
from shapely.geometry import shape
from shapely.geometry import box
from shapely.ops import polygonize_full
from descartes import PolygonPatch
from fiona import collection

features = collection("~/Desktop/gshhg-shp-2/GSHHS_shp/f/GSHHS_f_L1.shp")
northAmericaPolygon = shape(features[3]['geometry'])

api = overpy.Overpass()

stateRelation = api.query("rel(165475);(._;>;);out;")
fnwrRelation = api.query("rel(3947664);(._;>;);out;")
motorwaysInBoundingBox = api.query("way(32.120,-125.222,42.212,-113.928)[highway=motorway];(._;>);out;")
trunkInBoundingBox = api.query("way(32.120,-125.222,42.212,-113.928)[highway=trunk];(._;>);out;")
 
stateLineStrings = []
for way in stateRelation.ways:
 lineString = []
 for node in way.nodes:
  lineString.append((node.lon,node.lat))
 stateLineStrings.append(LineString(lineString))

polygons, dangles, cuts, invalids = polygonize_full(stateLineStrings)
statePolygonWithOcean = polygons.geoms[3]

statePolygon = statePolygonWithOcean.intersection(northAmericaPolygon)

fnwrLineStrings = []
for way in fnwrRelation.ways:
 lineString = []
 for node in way.nodes:
  lineString.append((node.lon,node.lat))
 fnwrLineStrings.append(LineString(lineString))

Fpolygons, dangles, cuts, invalids = polygonize_full(fnwrLineStrings)

motorwayLineStrings = []
for way in motorwaysInBoundingBox.ways:
 line = []
 for node in way.nodes:
  line.append((node.lon,node.lat))
 wayLineString = LineString(line)
 if statePolygonWithOcean.contains(wayLineString): motorwayLineStrings.append(wayLineString)

for way in trunkInBoundingBox.ways:
 line = []
 for node in way.nodes:
  line.append((node.lon,node.lat))
 wayLineString = LineString(line)
 if statePolygonWithOcean.contains(wayLineString): motorwayLineStrings.append(wayLineString)

islandPolygons = []
for i in range(0,len(polygons.geoms)):
 if (i != 3) and (i != 4):
  islandPolygons.append(polygons.geoms[i])

for geom in Fpolygons.geoms:
 islandPolygons.append(geom)

fig = pyplot.figure(figsize=(100,100))
ax = fig.add_subplot(111)

for line in motorwayLineStrings:
 x, y = line.xy
 ax.plot(x, y, color='#000000', linewidth=1, zorder=2)

patch = PolygonPatch(statePolygon, fc='#FFFFFF', ec='#000000', zorder=1)
ax.add_patch(patch)

for polygon in islandPolygons:
 patch = PolygonPatch(polygon, fc='#FFFFFF', ec='#000000', zorder=1)
 ax.add_patch(patch)

fig.savefig('test2.png')

##if we want more roads:
hgvInBoundingBox = api.query("way(32.120,-125.222,42.212,-113.928)[hgv=designated];(._;>);out;")
motorwayLineStrings = []
for way in hgvInBoundingBox.ways:
 line = []
 for node in way.nodes:
  line.append((node.lon,node.lat))
 wayLineString = LineString(line)
 if statePolygonWithOcean.contains(wayLineString): motorwayLineStrings.append(wayLineString)


##pickle
output = open('data.pkl', 'wb')
pickle.dump(islandPolygons,output)
pickle.dump(statePolygon,output)
pickle.dump(motorwayLineStrings,output)
output.close()

pkl_file = open('data.pkl', 'rb')
islandPolygons = pickle.load(pkl_file)
statePolygon = pickle.load(pkl_file)
motorwayLineStrings = pickle.load(pkl_file)
pkl_file.close()


##multiprocessing
from multiprocessing import Pool

def buildLineString(way):
 lineString = []
 for node in way.nodes:
  lineString.append((node.lon,node.lat))
 return lineString 

p = Pool(8)

for way in stateRelation.ways:
 stateLineStrings = p.map(buildLineString,stateRelation.ways)

features = collection("~/Desktop/gshhg-shp-2/GSHHS_shp/f/GSHHS_f_L1.shp")
northAmericaPolygon = shape(features[3]['geometry'])

api = overpy.Overpass()

stateRelation = api.query("rel(165475);(._;>;);out;")
fnwrRelation = api.query("rel(3947664);(._;>;);out;")
motorwaysInBoundingBox = api.query("way(32.120,-125.222,42.212,-113.928)[highway=motorway];(._;>);out;")

stateLineStrings = []
for way in stateRelation.ways:
 lineString = []
 for node in way.nodes:
  lineString.append((node.lon,node.lat))
 stateLineStrings.append(LineString(lineString))

## debug info
from geopandas import GeoSeries
from geopandas import GeoDataFrame

for i in range(0,len(islandPolygons)):
 ax.text(islandPolygons[i].centroid.x,islandPolygons[i].centroid.y,i,color = 'k', weight = 'bold')

ax.plot([-124.482003,-114.1307816],[32.5295236,42.009499])

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

Farallon National Wildlife Refuge (3947664)
Santa Catalina Island (237602)
San Clemente Island (237603)
Anacapa Island (3635899)
Santa Cruz Island (237600)
Santa Rosa Island (237601)
Way: Santa Barbara Island (40501085)
Way: Sutil Island (40501070)
Way: San Nicolas Island (40500976)
Way: San Miguel Island (40500912)

islandRelationNumbers = [3947664,237602,237603,3635899,237600,237601]
islandWayNumbers = [40501085,40501070,40500976,40500912]

islandRelations = []
for relation in islandRelationNumbers:
 response = api.query("rel(" + relation + ");(._;>;);out;")
 islandRelations.append(response)

islandWays = []
for ways in islandWayNumbers:
 response = api.query("way(" + way + ");(._;>;);out;")
 islandWays.append(response)

islandPolygons = []
for relation in islandRelations:
 islandLineStrings = []
 for way in relation.ways:
  lineString = []
  for node in way.nodes:
   lineString.append((node.lon,node.lat))
  islandLineStrings.append(LineString(lineString))
 polygons, dangles, cuts, invalids = polygonize_full(stateLineStrings)
 islandPolygons.append(polygons.geoms[0])

for way in islandWays:
 lineString = []
 for node in way.nodes:
  lineString.append((node.lon,node.lat))
 islandLineStrings.append(LineString(lineString))
 polygons, dangles, cuts, invalids = polygonize_full(stateLineStrings)
 islandPolygons.append(polygons.geoms[0])
