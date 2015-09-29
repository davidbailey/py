from os.path import expanduser
import pandas
import matplotlib.pyplot as plt
import numpy

df = pandas.DataFrame.from_csv(expanduser('~/Desktop/usc.csv'), index_col=False)

df.Country.value_counts() # total by country

for place in ['Gold', 'Silver', 'Bronze']: # g,s,b by sport
  print '\n\n', place, '\n'
  df[df['Place'] == place]['Sport'].value_counts()

df.Year.value_counts() # total per year

#df.Year.value_counts().sort_index().plot()
#plt.show()

def getColor(country):
  if country == "United States":
    return numpy.array((153, 0, 0)) / 255.0
  if country == "Great Britain":
    country = 'United Kingdom'
  if country == 'West Germany':
    country = 'Germany'
  if country in df.Country.value_counts():
    return numpy.array((255, 204, 0)) / 255.0
  else:
    return numpy.array((255,255,255)) / 255.0

from cartopy import crs
from cartopy.io import shapereader
countries = shapereader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
ax = plt.axes(projection=crs.PlateCarree())

for country in shapereader.Reader(countries).records():
  ax.add_geometries(country.geometry, crs.PlateCarree(), facecolor=getColor(country.attributes['name_long']))

plt.show()
