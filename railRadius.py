import geopandas
import overpass
import math

api = overpass.API()

name = 'Pacific Coast Highway'
response = api.Get('way["name"="' + name + '"]')
with open('temp.tmp', 'w') as f:
  f.write(str(response))

gdf = geopandas.read_file('temp.tmp')

def points2radius(pt1, pt2, pt3):
  a = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
  b = math.sqrt((pt2[0] - pt3[0])**2 + (pt2[1] - pt3[1])**2)
  c = math.sqrt((pt1[0] - pt3[0])**2 + (pt1[1] - pt3[1])**2)
  angleA = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
  angleB = math.degrees(math.acos((c**2 + a**2 - b**2) / (2 * c * a)))
  return max(angleA,angleB)

def geometry2maxradius(geometry):
  maxradius = 0
  for i in range(len(geometry.coords) - 2):
    if points2radius(geometry.coords[i], geometry.coords[i+1], geometry.coords[i+2]) > maxradius:
      maxradius = points2radius(geometry.coords[i], geometry.coords[i+1], geometry.coords[i+2])
  return maxradius

maxradius = lambda x: geometry2maxradius(x)
length = lambda x: math.sqrt((x.coords[0][0] - x.coords[-1][0])**2 + (x.coords[0][1] - x.coords[-1][1])**2)
segments = lambda x: len(x.coords)
gdf['maxradius'] = gdf['geometry'].map(maxradius)
gdf['length'] = gdf['geometry'].map(length)
gdf['segments'] = gdf['geometry'].map(segments)

la = gdf[gdf['tiger:county'] == 'Los Angeles, CA'][['maxradius', 'length', 'segments']]
la.sort_values('length')
