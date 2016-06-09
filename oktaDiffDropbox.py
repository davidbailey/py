import json
import requests

dropboxAPIToken = ""
oktaAPIToken = ""
oktaGroup = ""
oktaOrg = ""

dropboxUsers = []
r = requests.post("https://api.dropboxapi.com/2/team/members/list", headers={'Authorization': 'Bearer ' + dropboxAPIToken, 'Content-Type': 'application/json'}, data="{\"limit\": 700}" )
dropboxUsersJson =  r.json()
for user in dropboxUsersJson['members']:
  dropboxUsers.append(user['profile']['email'])

oktaUsers = []
r = requests.get("https://" + oktaOrg + ".okta.com/api/v1/groups/" + oktaGroup + "/users", headers={'Authorization': 'SSWS ' + oktaAPIToken})
oktaUsersJson =  r.json()
for user in oktaUsersJson:
  oktaUsers.append(user['profile']['login'])

inDropboxNotInOkta = set(dropboxUsers) - set(oktaUsers)
inOktaNotInDropbox = set(oktaUsers) - set(dropboxUsers)

print "These people are in Dropbox and not in Okta"
for user in inDropboxNotInOkta:
  print user

print "These people are in Okta and not in Dropbox"
for user in inOktaNotInDropbox :
  print user
