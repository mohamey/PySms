import urllib
import urllib2

log = open("../log.txt", 'wb')

def retrieveRemaining():
	request = urllib2.Request('https://webtexts.three.ie/webtext/messages/send')
	resp = urllib2.urlopen(request)
	dump = str(resp.read())
	position = dump.find("Remaining texts: ")
	rawRemaining = dump[(position+28):(position+32)]
	remaining = (rawRemaining.split(' '))[0]
	return remaining

##### Login to Three Ireland Website#####
def Login(details):

	login_url = 'https://webtexts.three.ie/webtext/users/login'

	payload = {
		'data[User][telephoneNo]' : details[0],
		'data[User][pin]' : details[1]
	}

	data = urllib.urlencode(payload)

	request = urllib2.Request(login_url, data)
	resp = urllib2.urlopen(request)
	contents = str(resp.geturl())

	if contents == 'https://webtexts.three.ie/webtext/messages/send':
		return True
	else:
		return False
		

def Send(msg, recipient):
	message_submission = 'https://webtexts.three.ie/webtext/messages/send'
	recipientCount = 0
	while recipientCount < len(recipient):
		payload = {
		'data[Message][message]' : msg,
		'data[Message][recipients_individual][0]' : recipient[recipientCount]
		}
		if recipientCount+1 < len(recipient):
			try:
				payload['data[Message][recipients_individual][1]'] = recipient[recipientCount+1]
			except:
				log.write("Unable to add contact 2")

			try:
				payload['data[Message][recipients_individual][2]'] = recipient[recipientCount+2]
			except:
				log.write("Unable to add contact 3")

		recipientCount = recipientCount+2

		data = urllib.urlencode(payload)	
		request = urllib2.Request(message_submission, data)
		resp = urllib2.urlopen(request)

	return True
