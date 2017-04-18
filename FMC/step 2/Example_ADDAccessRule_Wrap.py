#
# Generated FMC REST API sample script
#

import time
import sys
from WrapperAPI import Wrapper_API

server = "https://198.18.133.8"



ourRequest = Wrapper_API(server, username, password)

print "Authenticating..."
ourRequest.authentication()
print "Successful"

myURL = ourRequest.GETAccessRules()

 
iName = raw_input("Please choose a name for the Access Rule you would like to implement: ")
iAction = raw_input("Would you like this rule to ALLOW, DENY or MONITOR connections? ")
iLength = raw_input("How many seconds should this rule be implemented for? ")
iLength = int(iLength)

post_data = {
  "action": iAction,
  "enabled": "true",
  "type": "AccessRule",
  "name": iName,
  "sourceNetworks": {
    "objects": [
      {
        "type": "Network",
        "id" : "69fa2a3a-4487-4e3c-816f-4098f684826e"
      }
    ]
  },        "name": "any",

  "destinationNetworks": {
    "objects": [
      {
        "type": "Network",
        "name": "any",
        "id" : "69fa2a3a-4487-4e3c-816f-4098f684826e"
      }
    ]
  },
  "logFiles": "False",
  "logBegin": "False",
  "logEnd": "False"
}

myPost = ourRequest.PostApiCall(myURL, post_data)

if myPost["enabled"] == True:
    print ("The rule has now been implemented. The time is %s" % time.ctime())
    print "This rule will be in place for %i seconds" % iLength 


time.sleep(iLength)

newURL = myURL + "/" + myPost["id"]

deleter = ourRequest.DeleteApiCall(newURL)

if deleter == True:
    print "The rule has been deleted."


 
 
