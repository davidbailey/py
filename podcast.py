import pandas
import pafy
import requests
from cgi import escape
from urllib import urlencode
from email.Utils import formatdate
from bottle import route, run, template

music = pandas.read_csv('https://raw.githubusercontent.com/davidbailey/Notes/master/Music.csv')
#urls = ["https://www.youtube.com/watch?v=c2hkO5olZAg", "https://www.youtube.com/watch?v=KnddGSCu_WQ"]
urls = music[music['YouTube Link'].notnull()]

def getURL(url):
  try:
    video = pafy.new(url)
    video_url = video.getbest().url
    filesize = video.getbest().get_filesize()
    r = requests.get("http://tinyurl.com/api-create.php?" + urlencode({'url':video_url}))
    short_url = r.text
    return (short_url, filesize)
  except:
    return ('nourl', 0)
  
urls['urlfilesize'] = urls['YouTube Link'].apply(getURL)
#urls.to_csv()
rss = '<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" version="2.0"><channel><title>Localhost</title><language>en-US</language>'
timestamp = formatdate(0)
for index, row in urls.iterrows():
    rss += "<item>"
    rss += "<title>" + row['Song'] + "</title>"
    rss += "<pubDate>" + timestamp + "</pubDate>"
    rss += "<enclosure url=\"" + str(row['urlfilesize'][0]) + "\" length=\"" + str(row['urlfilesize'][1]) + "\" type=\"video/mp4\" />"
    rss += "</item>"

rss += "</channel></rss>"

@route('/podcast.xml')
def index():
  return rss

run(host='10.0.1.4', port=8080)
