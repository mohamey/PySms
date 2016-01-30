import vobject
from Tkinter import *
import keyring
from keyring import *
import cPickle
import tkMessageBox
import cookielib
import urllib
import urllib2
import atexit
import dependencies.three as three

####initialise url lib dependencies
cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
opener.addHeaders = [('User-agent', 'Webtext-Tool')]

urllib2.install_opener(opener)

log = open("log.txt", 'wb')

def closeFile(name):
	name.close()

atexit.register(closeFile, log)

def destroyGrid(frame):
	for widget in frame.grid_slaves():
		widget.destroy()

####Generate the Login Frame######
def generateLogin(frame):
	frame.wm_title("PySms")

	#####Save Login Details#######
	def saveLogin(login):
		try:
			fileObject = open("userData.txt", 'wb')
			keyring.set_password("Pysms", login[0], login[1])
			cPickle.dump(login[0], fileObject, protocol=cPickle.HIGHEST_PROTOCOL)
			fileObject.close()
		except:
			log.write("Failed To Save Login \n")

	#####Remove Login Details#####
	def purgeLogin(number):
		try:
			keyring.delete_password("Pysms", number)
			os.remove("userData.txt")
		except:
			log.write("Erro, unable to purge login data")

	######Check If Login Details already present#####
	def checkLogin():
		try:
			fileObject = open("userData.txt", 'r')
			loginDetails = cPickle.load(fileObject)
			if loginDetails:
				return loginDetails, keyring.get_password("Pysms", loginDetails)]
			return loginDetails
		except:
			log.write("No Login Details found on System")
			
	######Process Login Details#####
	def processLogin(phoneNumber, Password, saveDetails, retrieved):
		loginDetails = [phoneNumber, Password]
		if three.Login(loginDetails):
			if saveDetails == 1:
				saveLogin(loginDetails)
			elif ((saveDetails == 0) and (retrieved == True)):
				purgeLogin(phoneNumber)
			destroyGrid(frame)
			sendMessage(frame)
		else:
			tkMessageBox.showinfo('Login Failed', 'Please check your phone number and password and try again')

	PNLabel = Label(text="Phone number")
	PNLabel.grid(row=0, column=0, sticky="W")

	loginNumber = loginPassword = ""
	saveDetails = IntVar()
	storedDetails = checkLogin()
	retrieved = False

	if storedDetails:
		loginNumber = storedDetails[0]
		loginPassword = storedDetails[1]
		saveDetails.set(1)
		retrieved = True
	else:
		saveDetails.set(0)


	PhoneNumber = Entry(frame)
	PhoneNumber.insert(0, loginNumber)
	PhoneNumber.grid(row=0, column=1, padx=5, pady=5)

	PassLabel = Label(text="Password")
	PassLabel.grid(row=1, column=0, sticky="W")

	Password = Entry(show="*")
	Password.insert(END, loginPassword)
	Password.grid(row=1, column=1, padx=5, pady=5)


	checkSave = Checkbutton(text="Save My Login Details", variable=saveDetails, \
							onvalue=1, offvalue=0)
	checkSave.grid(row=2, column=0, columnspan=2, pady=5)


	B = Button(text="Login", command= lambda: processLogin(PhoneNumber.get(), Password.get(), saveDetails.get(), retrieved))
	B.grid(row=3, column=0, columnspan=2, pady=5)



#####Generate Send Message Frame
def sendMessage(frame):
	frame.wm_title("Send Message")

	numbers = []
	remainingTexts = -1
	try:
		remainingTexts = three.retrieveRemaining()
	except:
		log.write("Failed to Retrieve Webtext Amount")

	####Process Sending Messages 
	def processSend(msg, recipient):
		msgToSend = msg.strip()
		messageSize = (len(msgToSend) / 160)+1
		totalMessages = len(numbers) * messageSize
		if int(remainingTexts) > totalMessages:
			numbers.append(recipient)
			three.Send(msgToSend, numbers)
			tkMessageBox.showinfo('Success!', 'Your message was successfully sent!')
			destroyGrid(frame)
			sendMessage(frame)
		else:
			tkMessageBox.showinfo('Error', 'You do not have sufficient webtexts remaining to send this message')


	#event definition
	def update(event):
		if event.keycode == 8:
			message = msg.get("1.0", 'end-1c')
			var.set("Character Count: "+str(len(msg.get("1.0", 'end-2c'))))
		else:	
			var.set("Character Count: "+str(len(msg.get("1.0", 'end'))))

	def browseVcard(browseButton):
		from tkFileDialog import askopenfilename
		vcard = askopenfilename(filetypes=[("Vcards", "*.vcf")])
		display = str(vcard).split('/')
		browseButton.set(display[-1])
		fp = open(vcard, "r")
		content = fp.read()
		fp.close()

		vcards = vobject.readComponents(content)
		for contact in vcards:
			contact.prettyPrint()
			numbers.append(contact.tel.value)

	msgLabel = Label(text="Message")
	msgLabel.grid(row=0, column=0, sticky="W", padx=10)
	msg = Text(width=40, height=4, wrap="word", yscrollcommand="true")
	msg.grid(row=0, column=1, padx=10, pady=5)

	remainingLabel = Label(text="Remaining Webtexts: "+str(remainingTexts))
	remainingLabel.grid(row=1, column=0, padx= 5, sticky="E")

	var = StringVar()
	var.set("Character Count: 0")
	msg.bind("<Key>", update)
	charcount = Label(textvariable=var)
	charcount.grid(row=1, column=1, pady=3, padx=30, sticky="E")

	browseButton = StringVar()
	browseButton.set("Browse...")
	BrowseLabel = Label(text="Browse for Vcard")
	Browse = Button(textvar=browseButton, command = lambda: browseVcard(browseButton))
	BrowseLabel.grid(row=2, column=0, padx=10)
	Browse.grid(row=2, column=1, padx=10, sticky="W")	

	recipientLabel = Label(text="Recipient")
	recipientLabel.grid(row=3, column=0, padx=10, sticky="W")
	recipient = Entry()
	recipient.grid(row=3, column=1, padx=10, pady=10, sticky="W")

	C = Button(text="Send Message", command=lambda: processSend(msg.get("1.0", 'end-1c'), recipient.get()))
	C.grid(row = 4, column = 0, rowspan = 2, pady=5, columnspan=2)

if __name__ == '__main__':
	root = Tk()
	generateLogin(root)
	root.mainloop()