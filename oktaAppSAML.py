import requests
import json

# everything returns a 2xx on success and a 4xx on errors

oktaAPIToken = ""
oktaOrg = "org.oktapreview.com" # org.okta.com or org.oktapreview.com

headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'SSWS ' + oktaAPIToken}

data = {
  "name": "template_app",
  "label": "test-app",
  "signOnMode": "SAML_2_0",
  "settings": {
    "app": {
      "audienceRestriction": "http://localhost",
      "forceAuthn": False,
      "postBackURL": "http://localhost",
      "authnContextClassRef": "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport",
      "requestCompressed": "COMPRESSED",
      "recipient": "http://localhost",
      "signAssertion": "SIGNED",
      "destination": "http://localhost",
      "signResponse": "SIGNED",
      "nameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
      "groupName": "",
      "groupFilter": "",
      "defaultRelayState": "",
      "configuredIssuer": "",
      "attributeStatements": ""
      }
    },
  "visibility": {
      "hide": {
        "iOS": True,
        "web": True
    }
  }
}

r = requests.post("https://" + oktaOrg + "/api/v1/apps", headers = headers, data = json.dumps(data)) # create an app
appid = r.json()["id"]

appid = ""
r = requests.get("https://" + oktaOrg + "/api/v1/apps/" + appid , headers = headers) # view an app

groupid = ""
r = requests.put("https://" + oktaOrg + "/api/v1/apps/" + appid + "/groups/" + groupid, headers = headers, data = {}) # assign a group to an app

r = requests.post("https://" + oktaOrg + "/api/v1/apps/" + appid + "/lifecycle/deactivate", headers = headers) # deactivate an app (before deletion)

r = requests.delete("https://" + oktaOrg + "/api/v1/apps/" + appid , headers = headers) # delete an app
