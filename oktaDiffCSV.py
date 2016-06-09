from os.path import expanduser
import json
import requests
import pandas

oktaAPIToken = ""
oktaGroup = ""
oktaOrg = ""

appUsers = []
df = pandas.read_csv(expanduser('~/Desktop/users.csv'))
for email in df.index:
  appUsers.append(email)

oktaUsers = []
r = requests.get("https://" + oktaOrg + ".okta.com/api/v1/groups/" + oktaGroup + "/users", headers={'Authorization': 'SSWS ' + oktaAPIToken})
oktaUsersJson =  r.json()
for user in oktaUsersJson:
  oktaUsers.append(user['id'])

activeOktaUsers = []
for user in oktaUsers:
  r = requests.get("https://" + oktaOrg + ".okta.com/api/v1/users/" + user, headers={'Authorization': 'SSWS ' + oktaAPIToken})
  oktaUserJson =  r.json()
  if oktaUserJson['status'] == u'ACTIVE':
    activeOktaUsers.append(oktaUserJson['profile']['email'])

inAppNotInOkta = set(appUsers) - set(activeOktaUsers)
inOktaNotInApp = set(activeOktaUsers) - set(appUsers)

print "These people are in App and not in Okta"
for user in inAppNotInOkta:
  print user

print "These people are in Okta and not in App"
for user in inOktaNotInApp :
  print user
