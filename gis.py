import shapely.geometry
import matplotlib.pyplot as plt
import fiona.collection
import descartes

places = {'Los Angeles': (34.0204989,-118.4117325), 'Phoenix': (33.6054149,-112.125051), 'Albuquerque': (35.0824099,-106.6764794)}

path = [(x, y) for y, x in places.values()]
ls = shapely.geometry.LineString(path)

with fiona.collection("tl_2014_us_state/tl_2014_us_state.shp") as features:
    states = [shapely.geometry.shape(f['geometry']) for f in features]

fig = plt.figure(figsize=(8,5), dpi=180)
ax = fig.add_subplot(111)
ax.axis([-125, -65, 25, 50])
ax.axis('off')

ax.plot(*ls.xy, color='#FFFFFF')

for state in states:
 if state.geom_type =='Polygon':
  state = [state]
 for poly in state:
  poly_patch = descartes.PolygonPatch(poly, fc='#6699cc', ec='#000000')
  ax.add_patch(poly_patch)

for x, y in path:
 buffered = shapely.geometry.Point(x, y).buffer(1)
 ax.add_patch(descartes.PolygonPatch(buffered, fc='#EEEEEE', ec='#000000'))


fig.show()
