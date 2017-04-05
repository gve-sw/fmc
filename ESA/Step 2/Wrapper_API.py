import requests
import sys
import requests, base64
import json


#Next lines turn off messages about missing SSL certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class Wrapper_API(object):
	"""
	Initialisation for the class dealing with all calls to the FMC API
	"""
	def __init__(self, server, usrPass):
		b64Val = base64.b64encode(usrPass)

		self.server = server
		self.usrPass = b64Val
		self.headers = {'Content-Type': 'application/json', "Authorization": "Basic %s" % self.usrPass}
		self.api_base_path = "/api/v1.0/stats"
		self.json_resp = {}
		



	def GetDaily(self, url):
		"""
		Generic GET request to the ESA API with exception handling
		"""
		ApiPath = self.server + self.api_base_path + url
		try:
		    r = requests.get(ApiPath, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        print self.json_resp  
		        return self.json_resp  
		    else:
		        r.raise_for_status()
		        print("Error occurred in GET --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err)) 
		finally:
		    if r : r.close()



	def GetHighVolume(self, url):
		"""
		Generic GET request to the ESA API with exception handling
		"""
		ApiPath = self.server + self.api_base_path + url
		try:
		    r = requests.get(ApiPath, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        print self.json_resp  
		        return self.json_resp  
		    else:
		        r.raise_for_status()
		        print("Error occurred in GET --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err)) 
		finally:
		    if r : r.close()



	def GetIncomSum(self, url):
		"""
		Generic GET request to the ESA API with exception handling
		"""
		ApiPath = self.server + self.api_base_path + url
		try:
		    r = requests.get(ApiPath, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        print self.json_resp  
		        return self.json_resp  
		    else:
		        r.raise_for_status()
		        print("Error occurred in GET --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err)) 
		finally:
		    if r : r.close()


	def GetVirus(self, url):
		"""
		Generic GET request to the ESA API with exception handling
		"""
		ApiPath = self.server + self.api_base_path + url
		try:
		    r = requests.get(ApiPath, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        print self.json_resp  
		        return self.json_resp  
		    else:
		        r.raise_for_status()
		        print("Error occurred in GET --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err)) 
		finally:
		    if r : r.close()


	def GetSpecific(self, url):
		"""
		Generic GET request to the ESA API with exception handling
		"""
		ApiPath = self.server + self.api_base_path + url
		try:
		    r = requests.get(ApiPath, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        print self.json_resp  
		        return self.json_resp  
		    else:
		        r.raise_for_status()
		        print("Error occurred in GET --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err)) 
		finally:
		    if r : r.close()







