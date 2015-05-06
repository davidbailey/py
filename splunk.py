import socket
import splunklib.client as client
import splunklib.results as results
import re
import numpy as np
import pandas as pd
from geoip import geolite2
from ipwhois import IPWhois
import ipwhois

headers = [('address','user','user2','logontype','time','raw')]
data = []

get_address = lambda x: re.findall('(Source Network Address:\t)(.*?)(\n)',x)[0][1]
get_user = lambda x: re.findall('(Security ID:\t\t)(.*?)(\n)',x)[0][1]
get_user2 = lambda x: re.findall('(Security ID:\t\t)(.*?)(\n)',x)[1][1]
get_logontype = lambda x: re.findall('(Logon Type:\t\t\t)(.*?)(\n)',x)[0][1]
search = "search user EventCode=4624 | head 10"

service = client.connect(
    host="splunk.example.com",
    port=port,
    username="username",
    password="password")

socket.setdefaulttimeout(None)

response = service.jobs.oneshot(search)
reader = results.ResultsReader(response)

for result in reader:
 data.append((get_address(result['_raw']),get_user(result['_raw']),get_user2(result['_raw']),get_logontype(result['_raw']),result['_time'],result['_raw']))

df = pd.DataFrame(data)

for addr in df[0]:
 try:
  print socket.gethostbyaddr(addr)
 except socket.herror:
  print None, None, None
 try: 
  match = geolite2.lookup(addr)
  print match.country
 except AttributeError:
  print None
 try:
  print IPWhois(addr).lookup()
 except ipwhois.ipwhois.IPDefinedError:
  print None

