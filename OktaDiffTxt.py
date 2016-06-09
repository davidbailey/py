import json
import requests

oktaAPIToken = ""
oktaGroup = ""
oktaOrg = ""

appUsers = []
with open('appUsers.txt', 'r') as appFile:
  for line in appFile:
    appUsers.append(line.strip().lower())

oktaUsers = []
r = requests.get("https://" + oktaOrg + ".okta.com/api/v1/groups/" + oktaGroup + "/users", headers={'Authorization': 'SSWS ' + oktaAPIToken})
oktaUsersJson =  r.json()
for user in oktaUsersJson:
  oktaUsers.append(user['profile']['login'])

r = requests.get("https://" + oktaOrg + ".okta.com/api/v1/groups/" + oktaGroup2 + "/users", headers={'Authorization': 'SSWS ' + oktaAPIToken})
oktaUsersJson =  r.json()
for user in oktaUsersJson:
  oktaUsers.append(user['profile']['login'])

inAppNotInOkta = set(appUsers) - set(oktaUsers)
inOktaNotInApp = set(oktaUsers) - set(appUsers)

print "These people are in App and not in Okta"
for user in inAppNotInOkta:
  print user

print "These people are in Okta and not in App"
for user in inOktaNotInApp :
  print user
