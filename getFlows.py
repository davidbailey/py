from lxml import etree
from cStringIO import StringIO
import pycurl
import pandas as pd
import datetime

start = datetime.datetime(2014,9,19)
finish = datetime.datetime(2014,11,2)
delta = datetime.timedelta(hours=1)
times = []
while start <= finish:
 times.append(start)
 start += delta

for start in times:
 print start.strftime("%Y-%m-%dT%H:%M:%SZ")
 end = start + delta
 request1 = '<?xml version="1.0" encoding="UTF-8"?><soapenc:Envelope xmlns:soapenc="http://schemas.xmlsoap.org/soap/envelope/"><soapenc:Body><getFlows><flow-filter max-rows="100000" domain-id="133" include-interface-data="false">'
 request2 = '<date-selection><time-range-selection start="' + start.strftime("%Y-%m-%dT%H:%M:%SZ") + '" end="' + end.strftime("%Y-%m-%dT%H:%M:%SZ") + '" /></date-selection>'
 request3 = '<applications>175,53</applications>'
 request4 = '</flow-filter></getFlows></soapenc:Body></soapenc:Envelope>'
 request = request1 + request2 + request3 + request4
 buffer = StringIO()
 co = pycurl.Curl()
 co.setopt(co.UNRESTRICTED_AUTH,1)
 co.setopt(co.URL,"https://lancope.example.com/smc/swsService/flows")
 co.setopt(co.POST, 1)
 co.setopt(co.INFILESIZE,len(request) + 1) 
 co.setopt(co.WRITEFUNCTION, buffer.write)
 co.setopt(co.POSTFIELDS, request)
 co.setopt(co.SSL_VERIFYPEER, 0L) 
 co.setopt(co.SSL_VERIFYHOST, 0L) 
 co.setopt(co.USERPWD,"username:password")
 try:
  co.perform()
 except:
  print "POST failed"
  exit(1)

 co.close()
 out = buffer.getvalue()
 buffer.close()
 doc = etree.fromstring(out)
 netflows = [('client', 'clientHostName', 'clientPort', 'clientPackets', 'clientBytes', 'server', 'serverHostName', 'serverPort', 'serverPackets', 'serverBytes', 'startTime', 'lastTime', 'activeDuration')]
 for elem in doc.getiterator('{http://www.lancope.com/sws/sws-service}flow'):
  startTime = elem.get('start-time')
  lastTime = elem.get('last-time')
  activeDuration = elem.get('active-duration')
  client = elem[0].get('ip-address')
  clientHostName = elem[0].get('host-name')
  clientPort = elem[0].get('port')
  clientPackets = elem[0].get('packets')
  clientBytes = elem[0].get('bytes')
  server = elem[1].get('ip-address')
  serverHostName = elem[1].get('host-name')
  serverPort = elem[1].get('port')
  serverPackets = elem[1].get('packets')
  serverBytes = elem[1].get('bytes')
  netflows.append((client, clientHostName, clientPort, clientPackets, clientBytes, server, serverHostName, serverPort, serverPackets, serverBytes, startTime, lastTime, activeDuration))

 pd.DataFrame(netflows).to_csv(start.strftime("%Y-%m-%dT%H%M%SZ") + end.strftime("%Y-%m-%dT%H%M%SZ") + '.csv')
