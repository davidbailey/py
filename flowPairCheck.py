import pandas as pd
import numpy as np

clientHosts = ['0.0.0.0','1.1.1.1']
serverHosts = ['2.2.2.2','3.3.3.3']
netflowDF = pd.read_csv('netflow.csv', sep=',')

get = lambda  Num, clientHost, serverHost : '' if netflowDF[(netflowDF['Client Host'] == clientHost ) & (netflowDF['Server Host'] == serverHost)].empty else str(Num) + ','
hosts = []

for clientHost in clientHosts:
 match = ''
 for index, serverHost in enumerate(serverHosts):
  match += get(index, clientHost, serverHost)
 hosts.append((serverHost,match))

pd.DataFrame(hosts).to_csv('out.csv')
