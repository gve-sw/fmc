## Cisco Firepower Management Center - Application

Authors:
* Dan Kirkwood <dkirkwoo@cisco.com>
* Scott Ko <scoko@cisco.com>

April 2017

#### Instructions for use:
File AddURLtoBlocked.py contains an application which will take user input of a domain name and check the domain against the Umbrella Investigate API (more information [here](https://investigate-api.readme.io/).)

The application then gives the option of blocking or whitelisting the domain through the FMC URL filtering function, based on the result from Umbrella. 

**Note** that the application requires a settings.txt file containing the following: 
* Server ip address
* FMC username
* FMC password
* Token for access to the Umbrella API


> *These scripts are meant for educational purposes only. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.*