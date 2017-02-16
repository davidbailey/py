import pandas
import re
import os
import geopandas
import requests
from matplotlib import pyplot
import matplotlib
from biokit.viz import corrplot
from ftplib import FTP
import zipfile
import io
import pandas
from dbfread import DBF

# get mode share census data for one year from https://www.census.gov/data/developers/data-sets/acs-5year.html
modes = {'Total': 'B08006_001E', 'Car, truck, or van': 'B08006_002E', 'Drove alone': 'B08006_003E', 'Carpooled': 'B08006_004E', 'In 2-person carpool': 'B08006_005E', 'In 3-person carpool': 'B08006_006E', 'In 4-or-more-person carpool': 'B08006_007E', 'Public transportation (excluding taxicab)': 'B08006_008E', 'Bus or trolley bus': 'B08006_009E', 'Streetcar or trolley car (carro publico in Puerto Rico)': 'B08006_010E', 'Subway or elevated': 'B08006_011E', 'Railroad': 'B08006_012E', 'Ferryboat': 'B08006_013E', 'Bicycle': 'B08006_014E', 'Walked': 'B08006_015E', 'Taxicab, motorcycle, or other means': 'B08006_016E', 'Worked at home': 'B08006_017E'}
url = 'http://api.census.gov/data/2015/acs5?get=NAME,B01001_001E,' + ','.join(modes.values()) + '&for=county:*&in=state:06'
r = requests.get(url)
df = pandas.DataFrame(r.json())
df.columns = ['NAME','Population'] + list(modes) + ['state', 'county'] # or df.iloc[0]
df = df.drop(0)
for mode in modes.keys():
  df[mode + ' Rate'] = df[mode].apply(int) / df['Total'].apply(int) * 100

# get collision information from chp swirts
co = pandas.read_csv('CollisionRecords.txt')
injuries = {'NUMBER_KILLED': 'Total', 'COUNT_PED_KILLED': 'Walked', 'COUNT_PED_INJURED': 'Walked', 'COUNT_BICYCLIST_KILLED': 'Bicycle', 'COUNT_BICYCLIST_INJURED': 'Bicycle', 'COUNT_MC_KILLED': 'Taxicab, motorcycle, or other means', 'COUNT_MC_INJURED': 'Taxicab, motorcycle, or other means'}
for injury in list(injuries):
  df[injury] = df.index.map(lambda county: co[(int(county) * 100 <= co['CNTY_CITY_LOC']) & (co['CNTY_CITY_LOC'] < int(county) * 100 + 100)][injury].sum())

for injury, mode in injuries.items():
  df[injury + ' Rate'] = df[injury].apply(int) / df[mode].apply(int) * 100

df[['NAME','Bicycle','Bicycle Rate','COUNT_BICYCLIST_KILLED','COUNT_BICYCLIST_KILLED Rate']].sort_values(['Bicycle Rate'], ascending=False)

dft = df.convert_objects(convert_numeric=True)
# cor = list(set(injuries.values())) + list(injuries)
cor = list(modes) + list(injuries)
b = []
for a in cor:
  b.append(a + ' Rate') 
c = corrplot.Corrplot(dft[b])
matplotlib.rcParams.update({'font.size': 8})
c.plot()
pyplot.savefig('/Users/david/Desktop/fig.svg')
# pyplot.show()

# df.to_csv('modes.csv')

pyplot.scatter(df['Bicycle Rate'],df['COUNT_BICYCLIST_KILLED Rate'])
pyplot.show()

for county in df.index:
  print(df['NAME'][county])
  for injury in injuries:
    print(injury)
    co[(int(county) * 100 <= co['CNTY_CITY_LOC']) & (co['CNTY_CITY_LOC'] < int(county) * 100 + 100)][injury].sum()

gdf = geopandas.GeoDataFrame.from_file('/Users/david/Desktop/maps/tl_2010_06_county10/tl_2010_06_county10.shp')
df['NAMELSAD10'] = df.NAME.map(lambda county: county.split(',')[0])
dft = df.convert_objects(convert_numeric=True)
gdf = geopandas.GeoDataFrame(pandas.merge(dft,gdf))
gdf['COUNT_BICYCLIST_KILLED Rate'][1] = 25
gdf.plot(column='COUNT_BICYCLIST_KILLED Rate', cmap='OrRd')
gdf.plot(column='Bicycle Rate', cmap='OrRd')
pyplot.show()

# get mode share census data for one year from the past few years from https://www.census.gov/data/developers/data-sets/acs-5year.html
modes = {'Total': 'B08006_001E', 'Car, truck, or van': 'B08006_002E', 'Drove alone': 'B08006_003E', 'Carpooled': 'B08006_004E', 'In 2-person carpool': 'B08006_005E', 'In 3-person carpool': 'B08006_006E', 'In 4-or-more-person carpool': 'B08006_007E', 'Public transportation (excluding taxicab)': 'B08006_008E', 'Bus or trolley bus': 'B08006_009E', 'Streetcar or trolley car (carro publico in Puerto Rico)': 'B08006_010E', 'Subway or elevated': 'B08006_011E', 'Railroad': 'B08006_012E', 'Ferryboat': 'B08006_013E', 'Bicycle': 'B08006_014E', 'Walked': 'B08006_015E', 'Taxicab, motorcycle, or other means': 'B08006_016E', 'Worked at home': 'B08006_017E'}
years = range(2010,2016)
dfs = pandas.DataFrame(columns = ['NAME','Population'] + list(modes) + ['state', 'county', 'Year'])
for year in years:
  url = 'http://api.census.gov/data/' + str(year) + '/acs5?get=NAME,B01001_001E,' + ','.join(modes.values()) + '&for=county:*&in=state:06'
  r = requests.get(url)
  df = pandas.DataFrame(r.json())
  df.columns = ['NAME','Population'] + list(modes) + ['state', 'county'] # or df.iloc[0]
  df = df.drop(0)
  for mode in modes.keys():
    df[mode + ' Rate'] = df[mode].apply(int) / df['Total'].apply(int) * 100
  df['Year'] = year
  dfs = pandas.merge(dfs, df, how='outer')

df = dfs

# get collision data from chp swirts
co = pandas.read_csv('CollisionRecords.txt')
injuries = {'NUMBER_KILLED': 'Total', 'COUNT_PED_KILLED': 'Walked', 'COUNT_PED_INJURED': 'Walked', 'COUNT_BICYCLIST_KILLED': 'Bicycle', 'COUNT_BICYCLIST_INJURED': 'Bicycle', 'COUNT_MC_KILLED': 'Taxicab, motorcycle, or other means', 'COUNT_MC_INJURED': 'Taxicab, motorcycle, or other means'}
for injury in list(injuries):
  df[injury] = df.apply(lambda row: co[((int(row['county']) + 1) / 2* 100 <= co['CNTY_CITY_LOC']) & (co['CNTY_CITY_LOC'] < (int(row['county']) + 1) / 2 * 100 + 100) & (row['Year'] == co['ACCIDENT_YEAR'])][injury].sum(), axis=1)

for injury, mode in injuries.items():
  df[injury + ' Rate'] = df[injury].apply(int) / df[mode].apply(int) * 100

df[['NAME','Year','Bicycle','Bicycle Rate','COUNT_BICYCLIST_KILLED','COUNT_BICYCLIST_KILLED Rate']].sort_values(['Bicycle Rate'], ascending=False)

dft = df.convert_objects(convert_numeric=True)
# cor = list(set(injuries.values())) + list(injuries)
cor = list(modes) + list(injuries)
b = []
for a in cor:
  b.append(a + ' Rate') 
c = corrplot.Corrplot(dft[b])
matplotlib.rcParams.update({'font.size': 8})
c.plot()
pyplot.savefig('fig.svg')
# pyplot.show()

# df.to_csv('modes.csv')


pyplot.scatter(df[df['Year'] == 2015]['Bicycle Rate'], df[df['Year'] == 2015]['COUNT_BICYCLIST_KILLED Rate'].fillna(100), color='g')
pyplot.scatter(df[df['Year'] == 2015]['Walked Rate'], df[df['Year'] == 2015]['COUNT_PED_KILLED Rate'].fillna(100), color='b')
#pyplot.scatter(df['Bicycle Rate'], df['COUNT_BICYCLIST_KILLED Rate'].fillna(100), color='g')
#pyplot.scatter(df['Walked Rate'], df['COUNT_PED_KILLED Rate'].fillna(100), color='b')
ax = pyplot.gca()
ax.set_title('California Bicycle and Pedestrian Fatality Rate\nby Commute Rate per County(2015)')
ax.set_ylabel('Rate of Bicycle and Pedestrian Fatalities')
ax.set_xlabel('Rate of Bicycle and Pedestrian Commuters')
#pyplot.show(block=False)
#pyplot.tight_layout()
pyplot.savefig('plot.png')

for county in df.index:
  print(df['NAME'][county])
  for injury in injuries:
    print(injury)
    co[(int(county) * 100 <= co['CNTY_CITY_LOC']) & (co['CNTY_CITY_LOC'] < int(county) * 100 + 100)][injury].sum()

# plot on a map of california
gdf = geopandas.GeoDataFrame.from_file('tl_2010_06_county10/tl_2010_06_county10.shp')
df['NAMELSAD10'] = df.NAME.map(lambda county: county.split(',')[0])
dft = df.convert_objects(convert_numeric=True)
gdf = geopandas.GeoDataFrame(pandas.merge(dft,gdf))
gdf['COUNT_BICYCLIST_KILLED Rate'][1] = 25
gdf.plot(column='COUNT_BICYCLIST_KILLED Rate', cmap='OrRd')
gdf.plot(column='Bicycle Rate', cmap='OrRd')
pyplot.show()

''' fatalities based on collision data
fatality_count = co.groupby('ACCIDENT_YEAR').sum()[['COUNT_BICYCLIST_KILLED','COUNT_PED_KILLED','COUNT_MC_KILLED','NUMBER_KILLED']]
motorist_killed = lambda x: x['NUMBER_KILLED'] - x['COUNT_BICYCLIST_KILLED'] - x['COUNT_PED_KILLED'] - x['COUNT_MC_KILLED']
fatality_count['MOTORIST_KILLED'] = fatality_count.apply(motorist_killed, axis=1)
'''

vi = pandas.read_csv('VictimRecords.txt')
vico = pandas.merge(vi, co, how='left')
vi = vi.convert_objects(convert_numeric=True)
fatalsevere = vico[(vico['VICTIM_DEGREE_OF_INJURY'] == 1) | (vico['VICTIM_DEGREE_OF_INJURY'] == 2)].groupby(['ACCIDENT_YEAR', 'VICTIM_ROLE']).count()['CASE_ID']
fatalsevere.index.levels = [[2010, 2011, 2012, 2013, 2014, 2015], ['Driver', 'Passenger', 'Pedestrian', 'Bicyclist', 'Other']]
fatalsevere.index.names = ['Year', 'Victims by Mode ']

modeshare = dft.groupby('Year').sum()[['Total', 'Car, truck, or van', 'Walked', 'Bicycle']]
modeshare['Other'] = modeshare['Total'] - modeshare['Walked'] - modeshare['Bicycle'] - modeshare['Car, truck, or van'] 
modeshare.drop('Total', axis=1, inplace=True)
modeshare.columns = ['Car, truck, or van', 'Walk', 'Bicycle', 'Other']
modeshare = modeshare.stack()
modeshare.index.names = ['Year', 'Commuters by Mode']

colors = ['#AC7BE8', '#5CF24C', '#DB5531', '#4BA9F2', '#E8D342']
modeshare.unstack().plot.area(color = [colors[i] for i in [0,2,3,4]])
ax = pyplot.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.get_yaxis().get_major_formatter().set_scientific(False)
ax.set_title('California Commuters by Mode (2010-2015)')
ax.set_ylabel('People')
fatalsevere.unstack().plot.area(color = colors)
ax = pyplot.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.set_title('California Traffic Victims by Mode (2010-2015)')
ax.set_ylabel('People')
pyplot.show(block=False)

fatalsevere.loc[2015]/fatalsevere.loc[2015].sum()*100
modeshare.loc[2015]/modeshare.loc[2015].sum()*100

df = dfs
injuries = {3.0: 'Walked', 4.0: 'Bicycle'}
for injury in list(injuries):
  df[injury] = df.apply(lambda row: vico[((int(row['county']) + 1) / 2 * 100 <= vico['CNTY_CITY_LOC']) & (vico['CNTY_CITY_LOC'] < (int(row['county']) + 1) / 2 * 100 + 100) & (row['Year'] == vico['ACCIDENT_YEAR']) & ((vico['VICTIM_DEGREE_OF_INJURY'] == 1) | (vico['VICTIM_DEGREE_OF_INJURY'] == 2)) & (vico['VICTIM_ROLE'] == injury)]['CASE_ID'].count(), axis=1)

for injury, mode in injuries.items():
  df[str(injury) + ' Rate'] = df[injury].apply(int) / df[mode].apply(int) * 100

df[df['Year'] == 2015][['NAME','Year','Walked','Walked Rate',3.0,'3.0 Rate']].sort_values(['3.0 Rate'], ascending=False)
df[df['Year'] == 2015][['NAME','Year','Bicycle','Bicycle Rate',4.0,'4.0 Rate']].sort_values(['4.0 Rate'], ascending=False)

pyplot.scatter(df[df['Year'] == 2015]['Walked Rate'], df[df['Year'] == 2015]['3.0 Rate'].fillna(100), color='b')
pyplot.scatter(df[df['Year'] == 2015]['Bicycle Rate'], df[df['Year'] == 2015]['4.0 Rate'].fillna(100), color='g')
ax = pyplot.gca()
ax.set_title('California Bicycle and Pedestrian Fatality and Severe Injury Rate\nby Commute Rate per County(2015)')
ax.set_ylabel('Rate of Bicycle and Pedestrian Fatalities and Severe Injuries')
ax.set_xlabel('Rate of Bicycle and Pedestrian Commuters')
pyplot.show(block=False)
#pyplot.tight_layout()
#pyplot.savefig('plot.png')

from ftplib import FTP
import zipfile
import io
import pandas
from dbfread import DBF

# this bit doesn't work. need na update to the dbf package
def ftp2dataframe(url):
server = url.split('/')[2]
file = '/'.join(url.split('/')[3:])
data = io.BytesIO()
with FTP(server) as ftp:
  ftp.login()
  ftp.retrbinary('RETR ' + file, data.write)
zipFile = zipfile.ZipFile(data)
dfs = dict(zip(zipFile.namelist(),list(range(len(zipFile.namelist())))))
for name in zipFile.namelist():
  dbf_file = io.BytesIO(zipFile.open(name).read())
  dfs[name] = dbf2dataframe(dbf_file)
return dfs

def dbf2dataframe(dbf_file):
  dbf_list = []
  columns = []
  dbf_dbf = DBF(dbf_file)
  for row in dbf_dbf:
    columns = row.keys()
    dbf_list.append(row.values())
  return pandas.DataFrame(dbf_list, columns = columns)

url = 'ftp://ftp.nhtsa.dot.gov/fars/2015/National/FARS2015NationalDBF.zip'
data = ftp2dataframe(url)
data = dbf2dataframe('person.dbf')

states = {
1: "Alabama",
2: "Alaska",
4: "Arizona",
5: "Arkansas",
6: "California",
8: "Colorado",
9: "Connecticut",
10: "Delaware",
11: "District of Columbia",
12: "Florida",
13: "Georgia",
15: "Hawaii",
16: "Idaho",
17: "Illinois",
18: "Indiana",
19: "Iowa",
20: "Kansas",
21: "Kentucky",
22: "Louisiana",
23: "Maine",
24: "Maryland",
25: "Massachusetts",
26: "Michigan",
27: "Minnesota",
28: "Mississippi",
29: "Missouri",
30: "Montana",
31: "Nebraska",
32: "Nevada",
33: "New Hampshire",
34: "New Jersey",
35: "New Mexico",
36: "New York",
37: "North Carolina",
38: "North Dakota",
39: "Ohio",
40: "Oklahoma",
41: "Oregon",
42: "Pennsylvania",
43: "Puerto Rico",
44: "Rhode Island",
45: "South Carolina",
46: "South Dakota",
47: "Tennessee",
48: "Texas",
49: "Utah",
50: "Vermont",
52: "Virgin Islands",
51: "Virginia",
53: "Washington",
54: "West Virginia",
55: "Wisconsin",
56: "Wyoming"
}

person_types = { 1: 'Driver', 2: 'Passenger', 3: 'Passenger', 4: 'Other', 5: 'Pedestrian', 6: 'Bicyclist', 7: 'Bicyclist', 8: 'Other', 9: 'Passenger', 10: 'Other' }

df = dfs[dfs['Year'] == 2015]

injuries = {'Bicyclist': 'Bicycle', 'Pedestrian': 'Walked'}
#p = data['person.dbf'].replace({'STATE': states, 'PER_TYP': person_types})
p = data.replace({'STATE': states, 'PER_TYP': person_types})
p_people = p.groupby(['STATE', 'PER_TYP']).count()['PER_NO'].unstack()
p_people['NAME'] = p_people.index
pdf = pandas.merge(p_people, df)
pdf.fillna(0, inplace=True)

for injury, mode in injuries.items():
  pdf[injury + ' Rate'] = pdf[injury].apply(int) / pdf[mode].apply(int) * 100

pdf[['Bicycle Rate','Bicyclist Rate','NAME']].sort('Bicyclist Rate')
pdf[['Walked Rate','Pedestrian Rate','NAME']].sort('Pedestrian Rate')

pyplot.scatter(list(pdf['Walked Rate']), list(pdf['Pedestrian Rate']), color='b')
pyplot.scatter(list(pdf['Bicycle Rate']), list(pdf['Bicyclist Rate']), color='g')
ax = pyplot.gca()
ax.set_title('Bicycle and Pedestrian Fatalities \nby Commute Rate per State (2015)')
ax.set_ylabel('Rate of Bicycle and Pedestrian Fatalities')
ax.set_xlabel('Rate of Bicycle and Pedestrian Commuters')
pyplot.savefig('usrates.png')
pyplot.show(block=False)

modes = {'Total': 'B08006_001E', 'Car, truck, or van': 'B08006_002E', 'Drove alone': 'B08006_003E', 'Carpooled': 'B08006_004E', 'In 2-person carpool': 'B08006_005E', 'In 3-person carpool': 'B08006_006E', 'In 4-or-more-person carpool': 'B08006_007E', 'Public transportation (excluding taxicab)': 'B08006_008E', 'Bus or trolley bus': 'B08006_009E', 'Streetcar or trolley car (carro publico in Puerto Rico)': 'B08006_010E', 'Subway or elevated': 'B08006_011E', 'Railroad': 'B08006_012E', 'Ferryboat': 'B08006_013E', 'Bicycle': 'B08006_014E', 'Walked': 'B08006_015E', 'Taxicab, motorcycle, or other means': 'B08006_016E', 'Worked at home': 'B08006_017E'}
years = range(2015,2016)
dfs = pandas.DataFrame(columns = ['NAME','Population'] + list(modes) + ['state', 'Year'])
for year in years:
  url = 'http://api.census.gov/data/' + str(year) + '/acs5?get=NAME,B01001_001E,' + ','.join(modes.values()) + '&for=state:*'
  r = requests.get(url)
  df = pandas.DataFrame(r.json())
  df.columns = ['NAME','Population'] + list(modes) + ['state'] # or df.iloc[0]
  df = df.drop(0)
  for mode in modes.keys():
    df[mode + ' Rate'] = df[mode].apply(int) / df['Total'].apply(int) * 100
  df['Year'] = year
  dfs = pandas.merge(dfs, df, how='outer')

df = dfs
