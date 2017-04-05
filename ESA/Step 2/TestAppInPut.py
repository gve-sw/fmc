
import sys
from Wrapper_API import Wrapper_API

server = "http://198.18.133.146:6080"
usrPass = "admin:C1sco12345"


ourRequest = Wrapper_API(server, usrPass)

# Retrieve specific outgoing sender information based on given IP address 
Input_Ip= raw_input("Key in IP address you want to search : ")

ourRequest.GetSpecific("/mail_sender_ip_hostname_detail?duration=2016-12-01T00:00-00:00/2016-12-06T00:00-00:00&entity=" + Input_Ip +"&starts_with=true")

# Provide top X(Given by user) Maximum volume mails 
Input_num= raw_input("Please key in maximum number that you want to retrieve for high volume mails ")

ourRequest.GetHighVolume("/mail_subject_stats?duration=2016-12-01T00:00-00:00/2016-12-06T00:00-00:00&max=" + Input_num)

print "Successfully retrieve TOP" + Input_num +  "High volume"