#
# Generated FMC REST API sample script
#
 
import json
import sys
import requests
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
server = "https://198.18.133.8"
 
username = "admin"
if len(sys.argv) > 1:
    username = sys.argv[1]
password = "sf"
if len(sys.argv) > 2:
    password = sys.argv[2]
               
r = None
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
try:
    # 2 ways of making a REST call are provided:
    # One with "SSL verification turned off" and the other with "SSL verification turned on".
    # The one with "SSL verification turned off" is commented out. If you like to use that then 
    # uncomment the line where verify=False and comment the line with =verify='/path/to/ssl_certificate'
    # REST call with SSL verification turned off: 
    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
    # REST call with SSL verification turned on: Download SSL certificates from your FMC first and provide its path for verification.
    # r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify='/path/to/ssl_certificate')
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print ("Error in generating auth token --> "+str(err))
    sys.exit()
 
headers['X-auth-access-token']=auth_token
 
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/005056A0-025A-0ed3-0000-304942678240/accessrules"    # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]
 
# POST OPERATION
 
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
        "name": "any",
        "id" : "69fa2a3a-4487-4e3c-816f-4098f684826e"
      }
    ]
  },
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
try:
    # REST call with SSL verification turned off:
    r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.post(url, data=json.dumps(post_data), headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    #print("Status code is: "+str(status_code))
    if status_code == 201 or status_code == 202:
        print ("The rule has now been implemented. The time is %s" % time.ctime())
        print "This rule will be in place for %i seconds" % iLength
        json_resp = json.loads(resp)
        #print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else :
        r.raise_for_status()
        print ("Error occurred in POST --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err))
finally:
    if r: r.close()

           

time.sleep(iLength)
 
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/005056A0-025A-0ed3-0000-304942678240/accessrules/" + json_resp["id"]    # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

try:
    # REST call with SSL verification turned off:
    r = requests.delete(url, headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.delete(url, headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        #print("Delete successful. Response data --> ")
        print "The rule has been deleted. The time is %s" % time.ctime()
        json_resp = json.loads(resp)
        #print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else:
        r.raise_for_status()
        print("Error occurred in DELETE --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err))
finally:
    if r: r.close()
 


 
 
