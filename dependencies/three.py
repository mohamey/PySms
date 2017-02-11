import requests

globalSession = requests.Session()

###Login to the three website
def login(details):
	loginUrl = "https://webtexts.three.ie/users/login"
	payload = {
		'msisdn' : details[0],
		'pin' : details[1]
	}

	res = globalSession.post(loginUrl, data=payload)
	if res.url == "https://webtexts.three.ie/messages/send":
		print("Successful")
		return True
	else:
		print("Unsuccessful")
		return False

##Retrieve users remaining text messages
def retrieveRemaining():
	res = globalSession.get("https://webtexts.three.ie/webtext/messages/send")
	dump = res.text
	position = dump.find("Remaining texts: ")
	rawRemaining = dump[(position+28):(position+32)]
	remaining = (rawRemaining.split(' '))[0]
	return remaining

##Send messages, assuming we're logged in
def send(msg, recipient):
	messageSubmission = 'https://webtexts.three.ie/messages/send'
	recipientCount = 0
	while recipientCount < len(recipient):
		payload = {
			'message' : msg,
			'recipients_contacts[]' : recipient[recipientCount]
		}
		print(str(recipientCount+1) + " - " + str(len(recipient)))
		'''if recipientCount+1 < len(recipient):
			try:
				payload['data[Message][recipients_individual][1]'] = recipient[recipientCount+1]
			except:
				print("Unable to add contact 2")

			try:
				payload['data[Message][recipients_individual][2]'] = recipient[recipientCount+2]
			except:
				print("Unable to add contact 3")
'''
		recipientCount = recipientCount+1
		globalSession.post(messageSubmission, data=payload)

	return True
