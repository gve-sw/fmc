
import json
import sys
import requests, base64


usrPass = "admin:C1sco12345"
b64Val = base64.b64encode(usrPass)

server = "http://198.18.133.146:6080"
r = None

headers = {'Content-Type': 'application/json', "Authorization": "Basic %s" % b64Val}

#The following example shows how to retrieve aggregate Outgoing Sender report for IP addresses starting with 2001::6 for a specified duration

api_path = "/api/v1.0/stats/mail_sender_ip_hostname_detail?duration=2014-04-23T00:00-00:00/2014-10-21T00:00-00:00&entity=2001::63&starts_with=true"  # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

# GET OPERATION


try:
    # REST call with SSL verification turned off:
    r = requests.get(url, headers=headers, verify= False)
    # REST call with SSL verification turned on:
    #r = requests.get(url, headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        print("GET successful. Response data --> ")
        json_resp = json.loads(resp)
        print(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))
    else:
        r.raise_for_status()
        print("Error occurred in GET --> " + resp)
except requests.exceptions.HTTPError as err:
    print("Error in connection --> " + str(err))
finally:
    if r: r.close()
