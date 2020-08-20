import sys
import json 
from requests.auth import HTTPDigestAuth
import requests 

#TODO: Change the questions of username/password and auth token to params passed in at runtime 
#Cleaner code: Check if requests is installed. if not installed, install it with pip install requests. Also, figure out whats up with your local non-venv...
#remove the questions, set them as parameters passed in on runtime
#remove credentials and have them passed in at runtime
#Optional: json formatting!! and prettyfing and pygmenting 

baseURL = "https://stilettikate.atlassian.net/rest/api/3/issue/"

headers = {
  'Accept': 'application/json',
  #'Authorization': REDACTED
}
ticketheaders = {
  'Content-Type': 'application/json',
  #'Authorization': REDACTED
}

def searchForEpicTickets(username, apitoken, ticket, fixVersion):
	newurl = "https://stilettikate.atlassian.net/rest/api/3/search?jql=\"Epic%20Link\"%20%3D%20" + ticket
	response = requests.request("GET", newurl, headers=headers, data = {})
	response_data = response.json()
	print(response_data)
	for x in range(0, 2): # Need to update this for x = number of versions. whoops
		issue = response_data["issues"][x]["key"]
		print("Changing fixVersion for " + issue)
		url = baseURL + issue
		ticketVersionChange(username, apitoken, ticket, url, fixVersion)

def getTicket(username, apitoken, ticket, url, fixVersion):
	response = requests.request("GET", url, headers=headers, auth=HTTPDigestAuth(username, apitoken)) 
	jsonResponse = response.json()
	print(jsonResponse)
	if response.status_code != 200:    #add 201 202 etc. If they changed their API, it would need to be fixed 
		print ('Wrong ticket number, try again with a valid ticket number:. HTTP error: ' + str(response.status_code))
		exit()
	else:  
		issueType = jsonResponse["fields"]['issuetype']['name']
		if issueType == "Epic": 
			print("Starting jira search for all tickets in epic... ")
			searchForEpicTickets(username, apitoken, ticket, fixVersion)
		else: 
			print("This is identified as a single ticket (bug, task or story). Starting tagging fixVersion for this ticket only")	
			ticketVersionChange(username, apitoken, ticket, url, fixVersion)

def ticketVersionChange(username, apitoken, ticket, url, fixVersion):
	payload = "{\n    \"update\": {\n        \"fixVersions\" : [\n            {\"set\":\n                [\n                    {\"name\" : \"" + fixVersion + "\"}\n                ]\n            }\n        ]\n    }\n}"
	response = requests.request("PUT", url, headers=ticketheaders, data=payload)
	print("Your response is " + str(response.status_code))
	#test the change went through 
	testResponse = requests.request("GET", url, headers=headers, auth=HTTPDigestAuth(username, apitoken)) 
	jsonResponse = testResponse.json()
	fixVersionTest = jsonResponse["fields"]["fixVersions"][0]["name"]
	if fixVersionTest == fixVersion: 
		print("We queried the API again, and your fixVersion was changed! Good job. ")
	else: 
		print("Oops, it looks like something wrong, and your fixVersion was not set correctly. Make sure it's a valid fixVersion and try again! ")	

def main():
	username = input("What is your atlassian username? ")
	apitoken = input("What is your atlassian api token? ")
	ticket = input("Hello! Welcome to the fixVersion change app. \nWhat is your ticket number? Please list exactly as it reads in JIRA (I.e., APP-1111) ")
	fixVersion = input("What is the fixVersion? Please list exactly as it reads in JIRA (I.e., iOS Final Fantasy): ")
	url = baseURL + ticket
	getTicket(username, apitoken, ticket, url, fixVersion)

main()
