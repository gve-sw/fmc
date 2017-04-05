


#!/usr/bin/python

from urllib2 import Request, urlopen
import os, sys
import readSettings

setList = readSettings.loadSettings("../settings.txt")

token = setList[3].rstrip()

if not token:
  print "ERROR: environment variable \'INVESTIGATE_TOKEN\' not set. Invoke script with \'INVESTIGATE_TOKEN=%YourToken% python scripts.py\'"
  sys.exit(1)

# domains/categorization

headers = {
  'Authorization': 'Bearer ' + token
}
request = Request('https://investigate.api.opendns.com/domains/categorization/http://cisco.com', headers=headers)

response_body = urlopen(request).read()
print "domains/categorization: " + response_body