import sys
from WrapperAPI import Wrapper_API

server = "https://198.18.133.8"
username = "dkirkwoo"
password = "147760"


ourRequest = Wrapper_API(server, username, password)

print "Authenticating..."
ourRequest.authentication()
print "Successful"

domain = raw_input("Which domain would you like to block? ")


post_data = {
  "type": "Url",
  "overridable": False,
  "name": domain,
  "description": "testing",
  "url": domain
}

myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urls"

myPost = myPost = ourRequest.PostApiCall(myURL, post_data)

"""
put_data = {
  "id": "005056A0-025A-0ed3-0000-012884902447",
  "name": "URL-Filtering-Block",
  "type": "UrlGroup",
  "objects": [
    {
      "type": "Url"
    }
  ],
  "literals": [
    {
      "type": "Url",
      "url": domain
    }
  ]
}


myURL = server + "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/urlgroups/005056A0-025A-0ed3-0000-012884902447"


myPut = ourRequest.PutApiCall(myURL, put_data)

"""