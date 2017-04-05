import requests
import sys
import requests
import json


#Next lines turn off messages about missing SSL certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class Wrapper_API(object):
	"""
	Initialisation for the class dealing with all calls to the FMC API
	"""
	def __init__(self, server, username, password):
		self.server = server
		self.username = username
		self.password = password
		self.headers = {'Content-Type': 'application/json'}
		self.api_base_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f"
		self.json_resp = {}
		

	def authentication(self):
		"""
		Passes user and password to get a token for requests
		"""
		
		api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
		auth_url = self.server + api_auth_path

		try:
		    r = requests.post(auth_url, headers=self.headers, auth=requests.auth.HTTPBasicAuth(self.username,self.password), verify=False)
		    auth_headers = r.headers
		    auth_token = auth_headers.get('X-auth-access-token', default=None)
		    if auth_token == None:
		        print("auth_token not found. Exiting...")
		        sys.exit()
		except Exception as err:
		    print ("Error in generating auth token --> "+str(err))
		    sys.exit()
 
		self.headers['X-auth-access-token']=auth_token

		return self.headers


	def GetApiCall(self, url):
		"""
		Generic GET request to the FMC API with exception handling
		"""
		try:
		    r = requests.get(url, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        return self.json_resp    
		    else:
		        r.raise_for_status()
		        print("Error occurred in GET --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err)) 
		finally:
		    if r : r.close()

	
	def PostApiCall(self, url, post_data):
		"""
		Generic POST request to the FMC API with exception handling
		"""
		try:
		    r = requests.post(url, data=json.dumps(post_data), headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if status_code == 201 or status_code == 202:
		        #print ("The rule has now been implemented. The time is %s" % time.ctime())
		        #print "This rule will be in place for %i seconds" % iLength
		        self.json_resp = json.loads(resp)
		        return self.json_resp
		    else :
		        r.raise_for_status()
		        print ("Error occurred in POST --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err))
		finally:
		    if r: r.close()



	def PutApiCall(self, url, put_data):
		"""
		Generic PUT request to the FMC API with exception handling
		"""

		try:
		    r = requests.put(url, data=json.dumps(put_data), headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        self.json_resp = json.loads(resp)
		        print "Done"
		    else:
		        r.raise_for_status()
		        print("Status code:-->"+status_code)
		        print("Error occurred in PUT --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err))
		#finally:
		#   if r: r.close()
	    

	def DeleteApiCall(self, url):
		"""
		Generic DELETE request to the FMC API with exception handling
		"""

		try:
		    r = requests.delete(url, headers=self.headers, verify=False)
		    status_code = r.status_code
		    resp = r.text
		    if (status_code == 200):
		        #print "The rule has been deleted."
		        self.json_resp = json.loads(resp)
		        return True
		    else:
		        r.raise_for_status()
		        print("Error occurred in DELETE --> "+resp)
		except requests.exceptions.HTTPError as err:
		    print ("Error in connection --> "+str(err))
		finally:
		    if r: r.close()
 


	def printItems(self):
		"""
		Iterate over items from GET request and return their friendly names
		"""
		for i in range(len(self.json_resp["items"])):
		    print self.json_resp["items"][i]["name"]		


	def FindID(self,choice):
		"""
		Take a name as input and find the associated object ID
		"""
		for i in range(len(self.json_resp["items"])):
			if choice in self.json_resp["items"][i].values():
				object_id = self.json_resp["items"][i]["id"]	
		return object_id	

	def GETNetworkObjects(self):
		"""
		Returns all basic objects known to the FMC
		"""
		url = self.server + self.api_base_path + "/object/networks"

		self.GetApiCall(url)
		self.printItems()


	def GETObjects(self):
		"""
		Returns all network groups within the FMC
		"""
		url = self.server + self.api_base_path + "/object/networkgroups"

		self.GetApiCall(url)
		self.printItems()

	def GETAccessPolicies(self):
		"""
		Returns all Access Policies
		"""
		url = self.server + self.api_base_path + "/policy/accesspolicies"

		self.GetApiCall(url)
		self.printItems()
		


	def GETAccessRules(self):
		"""
		Returns all the rules associated with the chosen Access Policy
		"""
		self.GETAccessPolicies()

		choice = raw_input("Type the name of the Access Policy for which you would like to see the rules: ")

		container_id = self.FindID(choice)
				
		url = self.server + self.api_base_path + "/policy/accesspolicies/" + container_id + "/accessrules"

		self.GetApiCall(url)
		self.printItems()
		return url



	def CHANGEAccessRule(self):
		"""
		Enable or disable a chosen access rule
		"""
		accessurl = self.GETAccessRules()

		choice = raw_input("Type the name of rule which you would like to enable / disable: ")

		rule_id = self.FindID(choice)

		url = accessurl + "/" + rule_id

		self.GetApiCall(url)

		
		newBool = True

		if self.json_resp["enabled"] == True:
		    print choice + " will be DISABLED"
		    newBool = False
		else:
		    print choice + " will be ENABLED"  

		put_data = {
		  "action": self.json_resp["action"],
		  "enabled": newBool,
		  "type": self.json_resp["type"],
		  "name": self.json_resp["name"],
		  "id": self.json_resp["id"],
		  "sourceZones": self.json_resp["sourceZones"],
		  "destinationZones": self.json_resp["destinationZones"],
		  "logFiles": False,
		  "logBegin": False,
		  "logEnd": False,
		}

		self.PutApiCall(url, put_data)
		




if __name__ == '__main__':
	server = "https://198.18.133.8"
	username = "dkirkwoo"
	password = "147760"


	test = Wrapper_API(server, username, password)
	#test.authorization
