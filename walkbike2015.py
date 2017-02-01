import requests
import pandas
import geopandas

modes = {'Total': 'B08006_001E', 'Car, truck, or van': 'B08006_002E', 'Drove alone': 'B08006_003E', 'Carpooled': 'B08006_004E', 'In 2-person carpool': 'B08006_005E', 'In 3-person carpool': 'B08006_006E', 'In 4-o    r-more-person carpool': 'B08006_007E', 'Public transportation (excluding taxicab)': 'B08006_008E', 'Bus or trolley bus': 'B08006_009E', 'Streetcar or trolley car (carro publico in Puerto Rico)': 'B08006_010E', '    Subway or elevated': 'B08006_011E', 'Railroad': 'B08006_012E', 'Ferryboat': 'B08006_013E', 'Bicycle': 'B08006_014E', 'Walked': 'B08006_015E', 'Taxicab, motorcycle, or other means': 'B08006_016E', 'Worked at home    ': 'B08006_017E'}
url = 'http://api.census.gov/data/2015/acs5?get=B00001_001E,' + ','.join(modes.values()) + '&for=zip+code+tabulation+area:*'
r = requests.get(url)
df = pandas.DataFrame(r.json())
df.columns = ['B00001_001E'] + list(modes) + ['zip code tabulation area']
df = df.drop(0)

gdf = geopandas.GeoDataFrame.from_file('zcta5.geo.json') # from https://github.com/jgoodall/us-maps
cdf = pandas.merge(gdf, df, left_on='ZCTA5CE10', right_on='zip code tabulation area')
cdf = cdf.convert_objects(convert_numeric=True)

cdf['mode'] = cdf['Walked'] * 100 / cdf['Total']
bdf = cdf[['mode','geometry']]
bdf = bdf[bdf['mode'] > 5]
simplify = bdf['geometry'].simplify(100)
bdf['geometry'] = simplify

bdf.to_file('walked.js', driver='GeoJSON') # after this, add "var walked = " to the beginning of this file.
