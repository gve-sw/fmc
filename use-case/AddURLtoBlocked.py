#
#   Dan Kirkwood (dkirkwoo@cisco.com)
#   Scott Ko (scoko@cisco.com)
#       April 2017
#
#       This application checks a domain against the Umbrella Investigate API
#       then gives the option to block / whitelist the domain in FMC. 
#
#   REQUIREMENTS:
#       Python requests library (issue the 'pip install requests' command in shell or cmd)
#       Umbrella Investigate API access token
#
#   WARNING:
#       This script is meant for educational purposes only.
#       Any use of these scripts and tools is at
#       your own risk. There is no guarantee that
#       they have been through thorough testing in a
#       comparable environment and we are not
#       responsible for any damage or data loss
#       incurred with their use.
#
#   INFORMATION:
#       If you have further questions about this API and script, please contact GVE. Here are the contact details:
#           For internal Cisco gve-programmability@cisco.com
#           For Cisco partners, open a case at www.cisco.com/go/ph

import sys
from WrapperAPI import Wrapper_API
import requests
import json
import re
import readSettings

# Requires settings file containing FMC server, username, password and Umbrella API token
setList = readSettings.loadSettings("../settings.txt")

server = setList[0].rstrip()
username = setList[1].rstrip()
password = setList[2].rstrip()
token = setList[3].rstrip()

# Initialise the API class
ourRequest = Wrapper_API(server, username, password)

# Get an access token from the FMC API using the username and password provided
print "Authenticating..."
ourRequest.authentication()
print "Successful"

# Regex pattern to check user input for correct domain formatting
checker = re.compile('(http:\/\/)?(w{3})?(\.)?([a-zA-Z0-9]+)(\.)([a-z]{2,7})(\.)?([a-z]{2})?')

# Loop to check domain input
while True:
  domain = raw_input("Which domain would you like to check? ")
  if checker.match(domain):
    break  
  else:
    print "Not a domain name. Please try again."  


# Strip the http:// portion if provided
if domain.startswith('http://'):
  domain = domain[7:]


# Call the Umbrella Investigate API, find out how the domain is categorised and the status of the domain (trusted, untrusted, unknown)
headers = {
  'Authorization': 'Bearer ' + token
}
r_umbrella = requests.get('https://investigate.api.opendns.com/domains/categorization/' + domain + "?showLabels", headers=headers, verify=False)
resp = r_umbrella.text
json_response = json.loads(resp)


#End Umbrella check

print "\n"


# Return response to the user showing the status of the domain according to Umbrella
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


# Give the user the option to block whitelist or exit the program
decision = raw_input("Type BLOCK to block this domain on your FirePower device, WHITE to add it to the URL WhiteList or EXIT to exit: ")

if decision == "BLOCK":

  #First get the whole list of currently blocked sites. This is to prevent over-writing the block list when we add a new site
  currentBlocked = ourRequest.GETBlockedSites()
  
  #Create data type to add the individual URL to the FMC URL objects
  post_data = {
    "type": "Url",
    "overridable": False,
    "name": domain,
    "description": "testing",
    "url": domain
  }

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urls"

  # Post the indivvidual URL to the FMC to create a URL object based on the domain specified
  myPost = ourRequest.PostApiCall(myURL, post_data)


  existingURLs = currentBlocked["objects"]

  # Use the response from adding the URL to FMC to construct a new data type to update the blocked list
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

  # Add the new domain to the existing blocked domains
  newURLs["objects"] = newURLs["objects"] + existingURLs

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urlgroups/005056A0-025A-0ed3-0000-012884902447"

  # Send the data to FMC
  myPut = ourRequest.PutApiCall(myURL, newURLs)

elif decision == "WHITE":


  # Find the current URLs that are whitelisted to prevent this list from being overwritten by our new data
  currentWhite = ourRequest.GETWhiteList()


  # Construct data to add single URL to the FMC object store
  post_data = {
    "type": "Url",
    "overridable": False,
    "name": domain,
    "description": "testing",
    "url": domain
  }

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urls"

  # Add domain to the URL objects on FMC
  myPost = ourRequest.PostApiCall(myURL, post_data)

  existingURLs = currentWhite["objects"]

  # Use the response from adding the URL to FMC to construct a new data type to update the whitelist  
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

  # Add the new domain to the existing whitelisted domains
  newURLs["objects"] = newURLs["objects"] + existingURLs

  myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urlgroups/005056A0-025A-0ed3-0000-012884902372"

  # Send the data to FMC
  myPut = ourRequest.PutApiCall(myURL, newURLs)


# Exit program if requested by user
elif decision == "EXIT":
  exit()
