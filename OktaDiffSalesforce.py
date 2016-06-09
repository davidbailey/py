from os.path import expanduser
from suds.client import Client
import pandas
import re

sfurl = "https://org.my.salesforce.com/services/Soap/c/36.0/XXXXXXXXXXXXXXX"
username = ""
password = ""
security_token = ""

client = Client(expanduser('~/Desktop/enterprise.wsdl.xml'))
login_request = client.service.login(username, password+security_token)
client = Client(url=expanduser('~/Desktop/enterprise.wsdl.xml'), location=sfurl)
session_header = client.factory.create('SessionHeader')
session_header.sessionId = login_request['sessionId']
client.set_options(
    soapheaders = {
        'SessionHeader': session_header,
        })

soslQuery = "SELECT Id, IsActive, FirstName, LastName, Email, UserRoleId, ProfileId, UserPermissionsMarketingUser, UserPermissionsOfflineUser, UserPermissionsMobileUser, UserPermissionsSupportUser, UserPermissionsLiveAgentUser, UserPermissionsSFContentUser, UserPermissionsJigsawProspectingUser, UserPermissionsWorkDotComUserFeature, UserPermissionsKnowledgeUser, UserPermissionsInteractionUser FROM User" # I believe UserPermissionsSupportUser == Service Cloud User
User = client.service.query(soslQuery)

users = []
for user in User.records:
  if user.IsActive:
    try: users.append((user.Id, user.FirstName, user.LastName, user.Email, user.UserRoleId, user.ProfileId, user.UserPermissionsMarketingUser, user.UserPermissionsOfflineUser, user.UserPermissionsMobileUser, user.UserPermissionsSupportUser, user.UserPermissionsLiveAgentUser, user.UserPermissionsSFContentUser, user.UserPermissionsJigsawProspectingUser, user.UserPermissionsWorkDotComUserFeature, user.UserPermissionsKnowledgeUser, user.UserPermissionsInteractionUser))
    except: users.append((user.Id, user.FirstName, user.LastName, user.Email, "False", user.ProfileId, user.UserPermissionsMarketingUser, user.UserPermissionsOfflineUser, user.UserPermissionsMobileUser, user.UserPermissionsSupportUser, user.UserPermissionsLiveAgentUser, user.UserPermissionsSFContentUser, user.UserPermissionsJigsawProspectingUser, user.UserPermissionsWorkDotComUserFeature, user.UserPermissionsKnowledgeUser, user.UserPermissionsInteractionUser))

usersDF = pandas.DataFrame(users,columns=('userid', 'FirstName', 'LastName', 'Email', 'UserRoleId', 'ProfileId', 'UserPermissionsMarketingUser', 'UserPermissionsOfflineUser', 'UserPermissionsMobileUser', 'UserPermissionsSupportUser', 'UserPermissionsLiveAgentUser', 'UserPermissionsSFContentUser', 'UserPermissionsJigsawProspectingUser', 'UserPermissionsWorkDotComUserFeature', 'UserPermissionsKnowledgeUser', 'UserPermissionsInteractionUser'))

soslQuery = "SELECT Id, Name FROM UserRole"
UserRole = client.service.query(soslQuery)

roles = []
for role in UserRole.records:
  roles.append((role.Id, role.Name))

rolesDF = pandas.DataFrame(roles,columns=('UserRoleId','rolename'))

soslQuery = "SELECT Id, Name FROM Profile"
Profile = client.service.query(soslQuery)

profiles = []
for profile in Profile.records:
  profiles.append((profile.Id, profile.Name))

profilesDF = pandas.DataFrame(profiles,columns=('ProfileId','profilename'))

soslQuery = "SELECT Id, Assignee.Id, PermissionSet.Name FROM PermissionSetAssignment"
PermissionSetAssignment = client.service.query(soslQuery)

soslQuery = "SELECT Id, Name FROM PermissionSet"

permissionsetList = []
PermissionSets = client.service.query(soslQuery)
for permissionset in PermissionSets.records:
  soslQuery = "SELECT Id, Assignee.Id FROM PermissionSetAssignment WHERE PermissionSet.Id = '" + permissionset['Id'] + "'"
  PermissionSetAssignments = client.service.query(soslQuery)
  if PermissionSetAssignments.size > 0:
    permissionsetassignments = []
    for assignement in PermissionSetAssignments.records:
      permissionsetassignments.append(assignement.Assignee.Id)
    permissionsetList.append({permissionset['Name']: permissionsetassignments})

pattern = "X00.*"
permissionsetassignmentList = []
for user in usersDF.userid:
  userList = []
  for permissionset in permissionsetList:
    if user in permissionset.values()[0]:
      if not re.search(pattern, permissionset.keys()[0]):
        userList.append(permissionset.keys()[0])
  permissionsetassignmentList.append((user,userList))

permissionsetassignmentListDF = pandas.DataFrame(permissionsetassignmentList,columns=('userid','Permission Set List'))

soslQuery = "SELECT Id, GroupId, UserOrGroupId FROM GroupMember"
GroupMember = client.service.query(soslQuery)

groupmembers = []
for groupmember in GroupMember.records:
    groupmembers.append((groupmember.GroupId, groupmember.UserOrGroupId))

groupmembersDF = pandas.DataFrame(groupmembers,columns=('groupid','userorgroupid'))

soslQuery = "SELECT Id, Name, Type FROM Group"
Group = client.service.query(soslQuery)

groups = []
for group in Group.records:
  if group.Type == "Regular":
    groups.append((group.Id, group.Name))

groupsDF = pandas.DataFrame(groups,columns=('groupid','name'))

groupsAndgroupmembersDF = pandas.merge(groupsDF,groupmembersDF,how='left')

groupsList = []
for user in usersDF.userid:
  groupsList.append((user,groupsAndgroupmembersDF[groupsAndgroupmembersDF['userorgroupid'] == user]['name'].tolist()))

groupsListDF = pandas.DataFrame(groupsList,columns=('userid','Group List'))

usersAndRolesDF = pandas.merge(usersDF,rolesDF,how='left')
usersAndRolesAndProfilesDF = pandas.merge(usersAndRolesDF,profilesDF,how='left')
usersAndRolesAndProfilesAndpermissionsetassignmentListDF = pandas.merge(usersAndRolesAndProfilesDF,permissionsetassignmentListDF,how='left')
usersAndRolesAndProfilesAndpermissionsetassignmentListAndgroupsListDF = pandas.merge(usersAndRolesAndProfilesAndpermissionsetassignmentListDF,groupsListDF,how='left')
usersAndRolesAndProfilesAndpermissionsetassignmentListAndgroupsListDF.to_csv(expanduser('~/Desktop/salesforce_users.csv'))
df = usersAndRolesAndProfilesAndpermissionsetassignmentListAndgroupsListDF

import json
import requests

oktaAPIToken = ""
oktaOrg = ""
url = "https://" + oktaOrg + ".okta.com/api/v1/users?limit=200"
oktaUsers = []

while url:
  r = requests.get(url, headers={'Authorization': 'SSWS ' + oktaAPIToken})
  oktaUsersJson =  r.json()
  for user in oktaUsersJson:
    try: oktaUsers.append([user['profile']['login'], user['profile']['title']])
    except: print user['profile']['login']
  try: url = r.links['next']['url']
  except: url = False

oktaDF = pandas.DataFrame(oktaUsers,columns=('Email','orgID','title'))
okta_sf_DF = pandas.merge(df,oktaDF,how='right')
okta_sf_DF.to_csv(expanduser('~/Desktop/okta_salesforce_users.csv'))
