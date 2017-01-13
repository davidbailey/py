import pandas
from matplotlib import pyplot

urls = {
 2015: 'http://dot.ca.gov/trafficops/census/docs/2015aadt.xls',
 2014: 'http://dot.ca.gov/trafficops/census/docs/2014aadt.xlsx',
 2013: 'http://dot.ca.gov/trafficops/census/docs/2013aadt.xlsx',
 2012: 'http://dot.ca.gov/trafficops/census/docs/2012aadt.xlsx',
 2011: 'http://dot.ca.gov/trafficops/census/docs/2011aadt.xlsx'
}

columns = ['District', 'Route Number', 'x1', 'County', 'Milepost Prefix', 'Milepost', 'x2', 'Description', 'Back Peak Hour', 'Back Peak Month', 'Back AADT', 'Ahead Peak Hour', 'Ahead Peak Month', 'Ahead AADT']

aadt = pandas.DataFrame(columns = columns)
for year, url in urls.items():
  df = pandas.read_excel(url)
  df.columns = columns
  df['Year'] = year
  aadt = pandas.merge(aadt, df, how='outer')

aadt = aadt.convert_objects(convert_numeric=True) # some numbers (e.g. 405) are sometimes strings and sometimes numbers

mileposts = {
  30.856: 'Santa Monica Bl.',
  31.542: 'Wilshire',
  32.502: 'Waterford/Montana',
  32.996: 'Sunset',
  33.290: 'Moraga',
  34.764: 'Getty Center Dr.',
  37.026: 'Mulholland',
  39.432: '101',
  40.285: 'Burbank Bl.'
}

aadt['Milepost'] = aadt['Milepost'].round(3) # some floats get imported funky
plotdf = aadt[(aadt['Route Number'] == 405) & (aadt['Milepost'].isin(mileposts.keys()))][['Milepost', 'Year', 'Back AADT']] # select column to plot
plotdf.sort_values(['Milepost', 'Year'], inplace=True)
plotdf.set_index('Year', inplace=True)
fig = pyplot.figure()
for i, milepost in enumerate(mileposts.keys()):
  ax = fig.add_subplot(3,3,1 + i)
  plotdf[plotdf['Milepost'] == milepost].plot.bar(ax=ax, legend=False)
  # ax.set_ylim(plotdf[plotdf['Milepost'] == milepost]['Back AADT'].min() - 2000, plotdf[plotdf['Milepost'] == milepost]['Back AADT'].max() + 2000) # uncomment to distort axis and zoom in
  ax.set_title(mileposts[milepost])
  ax.set_ylabel('Vehicles/Hour')

pyplot.style.use('ggplot')
pyplot.tight_layout()
fig.savefig('back_aadt_zoom.png') # filename
pyplot.show()
