from os.path import expanduser
from suds.client import Client
import pandas

stg = pandas.read_csv(expanduser('~/Desktop/salesforce-stg.csv'))
prod = pandas.read_csv(expanduser('~/Desktop/salesforce-prod.csv'))

removeBits = lambda x: x.split("=")[0].split("@")[0]

stg['Prefix'] = stg['Email'].map(removeBits)
prod['Prefix'] = prod['Email'].map(removeBits)

usersToDisablePrefixes = pandas.DataFrame(list(set(stg['Prefix']) - set(prod['Prefix'])), columns=['Prefix'])
usersToDisableDF = pandas.merge(stg, usersToDisablePrefixes)
usersToDisable = list(usersToDisableDF['userid'])

sfurl = "https://org.my.salesforce.com/services/Soap/c/36.0/XXXXXXXXXXXXXXX"
username = ''
password = ''
security_token = ''

client = Client(expanduser('~/Desktop/stg.enterprise.wsdl.xml'))
login_request = client.service.login(username, password+security_token)
client = Client(url=expanduser('~/Desktop/stg.enterprise.wsdl.xml'), location=sfurl)
session_header = client.factory.create('SessionHeader')
session_header.sessionId = login_request['sessionId']
client.set_options(
    soapheaders = {
        'SessionHeader': session_header,
        })  

for userid in usersToDisable:
  soslQuery = "SELECT Id, IsActive FROM User WHERE Id='" + userid + "'"
  User = client.service.query(soslQuery)
  user = User.records[0]
  user.IsActive = False
  client.service.update(user)
