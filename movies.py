import pandas
import requests

movies = pandas.read_csv('https://raw.githubusercontent.com/davidbailey/Notes/master/Movies.csv')

for movie in movies.Title:
  r = requests.get('https://www.omdbapi.com/?t=' + movie)
  print(r.json()['Title'], r.json()['Year'])
