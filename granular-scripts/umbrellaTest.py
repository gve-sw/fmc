


#!/usr/bin/python

from urllib2 import Request, urlopen
import os, sys

token = "268f72e1-b0b4-4d74-b0c2-ea99320b1ff9"

if not token:
  print "ERROR: environment variable \'INVESTIGATE_TOKEN\' not set. Invoke script with \'INVESTIGATE_TOKEN=%YourToken% python scripts.py\'"
  sys.exit(1)

# domains/categorization

headers = {
  'Authorization': 'Bearer ' + token
}
request = Request('https://investigate.api.opendns.com/domains/categorization/amazon.com', headers=headers)

response_body = urlopen(request).read()
print "domains/categorization: " + response_body