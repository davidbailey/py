import pandas
import geopandas
import requests

def TripGeneration():
  originDestinationFile = '/Users/david/Desktop/maps/ca_od_2013/ca_od_main_JT0.csv'
  originDestination = pandas.DataFrame.from_csv(originDestinationFile)
  originDestination.reset_index(inplace=True)
  return originDestination

def TripDistribution(originDestination):
  censusTractsFile = '/Users/david/Desktop/maps/tl_2010_06_tract10/tl_2010_06_tract10.shp'
  censusTracts = geopandas.GeoDataFrame.from_file(censusTractsFile)
  censusTracts.set_index('GEOID10', inplace=True)
  # censusTracts2GEOMETRY = lambda x: censusTracts.loc['0' + str(x)[:10]]['geometry']
  censusTracts2LatLonH = lambda x: [float(censusTracts.loc['0' + str(x)[:10]]['INTPTLAT10']), float(censusTracts.loc['0' + str(x)[:10]]['INTPTLON10'])]
  censusTracts2LatLonW = lambda x: [float(censusTracts.loc[str(x)[:11]]['INTPTLAT10']), float(censusTracts.loc[str(x)[:11]]['INTPTLON10'])]
  originDestination['hLatLon'] = originDestination['h_geocode'].apply(censusTracts2LatLonH)
  originDestination['wLatLon'] = originDestination['w_geocode'].apply(censusTracts2LatLonW)
  return originDestination

def modeChooser(row):
  alpha = 900
  beta = 600
  gamma = 900
  if (row['foot']['routes'][0]['duration'] - gamma < row['bicycle']['routes'][0]['duration']) & (row['foot']['routes'][0]['duration'] - alpha < row['car']['routes'][0]['duration']):
    return 'foot'
  elif row['bicycle']['routes'][0]['duration'] - beta < row['car']['routes'][0]['duration']:
    return 'bicycle'
  else: 
    return 'car'

def ModeChoice(originDestination):
  foot = lambda x: requests.get('http://localhost:5000/route/v1/foot/' + str(x['hLatLon'][1]) + ',' + str(x['hLatLon'][0]) + ';' + str(x['wLatLon'][1]) + ',' + str(x['wLatLon'][0])).json()
  bicycle = lambda x: requests.get('http://localhost:5001/route/v1/bike/' + str(x['hLatLon'][1]) + ',' + str(x['hLatLon'][0]) + ';' + str(x['wLatLon'][1]) + ',' + str(x['wLatLon'][0])).json()
  car = lambda x: requests.get('http://localhost:5002/route/v1/car/' + str(x['hLatLon'][1]) + ',' + str(x['hLatLon'][0]) + ';' + str(x['wLatLon'][1]) + ',' + str(x['wLatLon'][0])).json()
  originDestination['foot'] = originDestination.apply(foot, axis=1)
  originDestination['bicycle'] = originDestination.apply(bicycle, axis=1)
  originDestination['car'] = originDestination.apply(car, axis=1)
  originDestination['mode'] = originDestination.apply(modeChooser, axis=1)
  return originDestination

def RouteAssignment(originDestination):
  travelTime = lambda x: x[x['mode']]['routes'][0]['duration']
  originDestination['travelTime'] = originDestination.apply(travelTime, axis=1)
  return originDestination

if __name__ == "__main__":
  originDestination = TripGeneration()
  originDestination = TripDistribution(originDestination)
  originDestination = ModeChoice(originDestination)
  originDestination = RouteAssignment(originDestination)
  # sum up the number of people on each route
  modeShare = originDestination['mode'].value_counts()
  averageTravelTime = originDestination['travelTime'].sum() / len(a) 
