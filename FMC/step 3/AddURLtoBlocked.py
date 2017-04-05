import sys
from WrapperAPI import Wrapper_API
import requests
import json
import re
import readSettings

setList = readSettings.loadSettings("../settings.txt")

server = setList[0].rstrip()
username = setList[1].rstrip()
password = setList[2].rstrip()
token = setList[3].rstrip()


ourRequest = Wrapper_API(server, username, password)

print "Authenticating..."
ourRequest.authentication()
print "Successful"


checker = re.compile('(http:\/\/)?(w{3})?(\.)?([a-zA-Z0-9]+)(\.)([a-z]{2,7})(\.)?([a-z]{2})?')

while True:
  domain = raw_input("Which domain would you like to check? ")
  if checker.match(domain):
    break  
  else:
    print "Not a domain name. Please try again."  

if domain.startswith('http://'):
  domain = domain[7:]


#Umbrella Investigate API
headers = {
  'Authorization': 'Bearer ' + token
}
r_umbrella = requests.get('https://investigate.api.opendns.com/domains/categorization/' + domain + "?showLabels", headers=headers, verify=False)
resp = r_umbrella.text
json_response = json.loads(resp)


#End Umbrella check
print "\n"

if json_response[domain]['status'] == 1:
  print "This domain is beleived to be safe."
elif json_response[domain]['status'] == 0:
  print "This domain has not yet been classified by Umbrella."
elif json_response[domain]['status'] == -1:
  print "This domain is believed to be malicious. Block reccomended."

if len(json_response[domain]['content_categories']) != 0:
  print "\n"
  print "Domain categories: "

  for i in json_response[domain]['content_categories']:
    print "    " + i

print "\n"

decision = raw_input("Type BLOCK to block this domain on your FirePower device, WHITE to add it to the URL WhiteList or EXIT to exit: ")

if decision == "BLOCK":

  currentBlocked = ourRequest.GETBlockedSites()
  
  post_data = {
    "type": "Url",
    "overridable": False,
    "name": domain,
    "description": "testing",
    "url": domain
  }

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urls"

  myPost = ourRequest.PostApiCall(myURL, post_data)

  existingURLs = currentBlocked["objects"]

  newURLs ={
    "id": "005056A0-025A-0ed3-0000-012884902447",
    "name": "URL-Filtering-Block",
    "type": "UrlGroup",
    "objects": [
      {
        "type": "Url",
        "id": myPost["id"]
      }
    ]
  }

  newURLs["objects"] = newURLs["objects"] + existingURLs

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urlgroups/005056A0-025A-0ed3-0000-012884902447"

  myPut = ourRequest.PutApiCall(myURL, newURLs)

elif decision == "WHITE":

  currentWhite = ourRequest.GETWhiteList()

  post_data = {
    "type": "Url",
    "overridable": False,
    "name": domain,
    "description": "testing",
    "url": domain
  }

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urls"

  myPost = ourRequest.PostApiCall(myURL, post_data)

  existingURLs = currentWhite["objects"]

  newURLs ={
    "id": "005056A0-025A-0ed3-0000-012884902372",
    "name": "URL-Filtering-Whitelist",
    "type": "UrlGroup",
    "objects": [
      {
        "type": "Url",
        "id": myPost["id"]
      }
    ]
  }

  newURLs["objects"] = newURLs["objects"] + existingURLs

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urlgroups/005056A0-025A-0ed3-0000-012884902372"

  myPut = ourRequest.PutApiCall(myURL, newURLs)


elif decision == "EXIT":
  exit()
