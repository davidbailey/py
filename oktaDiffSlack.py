import json
import requests

slackAPIToken = ""
oktaAPIToken = ""
oktaGroup = ""
oktaOrg = ""

slackDeleted = []
slackBots = []
slackRestricted = []
slackUsers = []
r = requests.get("https://slack.com/api/users.list?token=" + slackAPIToken)
slackUsersJson =  r.json()
for user in slackUsersJson['members']:
  if (user['deleted'] == True): slackDeleted.append(user['profile']['real_name'])
  elif (user['is_bot'] == True): slackBots.append(user['profile']['real_name'])
  elif (user['is_restricted'] == True): slackRestricted.append(user['profile']['real_name'])
  else: slackUsers.append(user['profile']['email'])

oktaUsers = []
r = requests.get("https://" + oktaOrg + ".okta.com/api/v1/groups/" + oktaGroup + "/users", headers={'Authorization': 'SSWS ' + oktaAPIToken})
oktaUsersJson =  r.json()
for user in oktaUsersJson:
  oktaUsers.append(user['profile']['login'])

inSlackNotInOkta = set(slackUsers) - set(oktaUsers)
inOktaNotInSlack = set(oktaUsers) - set(slackUsers)

print "These people are in Slack and not in Okta"
for user in inSlackNotInOkta:
  print user

print "These people are in Okta and not in Slack"
for user in inOktaNotInSlack :
  print user
