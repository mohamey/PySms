from Tkinter import *
from splinter import Browser
import json
import tkMessageBox
import vobject

#Global Variables
loggedin = False;
browser = Browser('phantomjs')
vcard = ""
message = ""
numbers = []

###Store user details in shelve database

def saveLogin(phone, password):
	login = [phone, password]
	file_name="userData"
	fileObject = open(file_name, 'wb')
	json.dump(login, fileObject)
	fileObject.close()

def checkLogin():
	try:
		fileObject = open("userData", 'r')
		loginDetails = json.load(fileObject)
		return loginDetails
	except:
		pass

##############LOGIN TO THREE WEBSITE##############
def login(frame):

	###Attempt Login to Website####
	def attemptLogin(phone, password, saveDetails):
		url = "https://webtexts.three.ie"
		browser.visit(url)
		browser.fill('data[User][telephoneNo]', phone)
		browser.fill('data[User][pin]', password)
		browser.find_by_css('a.trigger-submit').first.click()
		print browser.url
		if browser.url == "https://webtexts.three.ie/":
			tkMessageBox.showinfo("Oh no :O", "You have entered an invalid phone number/password")
		else:
			if saveDetails == 1:
				saveLogin(phone, password)
			for widget in frame.grid_slaves():
				widget.destroy()
			print "Grid Destroyed"
			sendMessage(root)

	loginDetails = checkLogin()
	if not loginDetails:
		loginNumber = loginPassword = ""
		print "beginning login screen"
		PNLabel = Label(text="Phone number")
		PNLabel.grid(row=0, column=0, sticky="W")

		print "Beginning phone number entry"
		print loginNumber
		PhoneNumber = Entry(frame)
		PhoneNumber.insert(0, loginNumber)
		PhoneNumber.grid(row=0, column=1, padx=5, pady=5)

		print "Beginning PassLabel Entry"
		PassLabel = Label(text="Password")
		PassLabel.grid(row=1, column=0, sticky="W")

		print "Beginning Password Entry"
		Password = Entry(show="*")
		Password.insert(END, loginPassword)
		Password.grid(row=1, column=1, padx=5, pady=5)

		saveDetails = IntVar()
		saveDetails.set(0)

		print "Creating Checkbox"
		checkSave = Checkbutton(text="Save My Login Details", variable=saveDetails, \
								onvalue=1, offvalue=0)
		checkSave.grid(row=2, column=0, columnspan=2, pady=5)

		print str(saveDetails.get())

		print "Creating login button"
		B = Button(text="login", command= lambda: attemptLogin(PhoneNumber.get(), Password.get(), saveDetails.get()))
		B.grid(row=3, column=0, columnspan=2, pady=5)
	else:
		print "Logging in"
		loggingIn = Message(text="Logging in...")
		loggingIn.grid()
		loginNumber = ""+loginDetails[0]
		loginPassword = ""+loginDetails[1]
		attemptLogin(loginNumber, loginPassword, 0)

def sendMessage(frame):

	#event definition
	def update(event):
		print str(event.keycode)
		if event.keycode == 8:
			print "backspace detected"
			message = msg.get("1.0", 'end-1c')
			var.set("Character Count: "+str(len(msg.get("1.0", 'end-2c'))))
		else:	
			var.set("Character Count: "+str(len(msg.get("1.0", 'end'))))
			print "Normal key inputted"

	def browseVcard(browseButton):
		from tkFileDialog import askopenfilename
		#frame.withdraw()
		vcard = askopenfilename(filetypes=[("Vcards", "*.vcf")])
		browseButton.set(vcard)
		fp = open('test.vcf', "r")
		content = fp.read()
		fp.close()

		vcards = vobject.readComponents(content)
		for contact in vcards:
			contact.prettyPrint()
			numbers.append(contact.tel.value)

	def send(message, recipient):
		numbers.append(recipient)
		count = 0;
		while (count < len(numbers)):
			browser.fill('data[Message][message]', message)
			browser.fill('data[Message][recipients_individual][0]', numbers[count])
			try:
				browser.fill('data[Message][recipients_individual][1]', numbers[count+1])
			except:
				pass
			try:
				browser.fill('data[Message][recipients_individual][2]', numbers[count+2])
			except:
				pass
			count = count+3
			browser.find_by_css('a.trigger-submit').first.click()
		tkMessageBox.showinfo("Message Sent :D", "Your message has been successfully sent!")
		for widget in frame.grid_slaves():
			widget.destroy()
		print "Grid Destroyed"
		sendMessage(root)


	print "Entered send message"
	msgLabel = Label(text="Message")
	msgLabel.grid(row=0, column=0, sticky="W", padx=10)
	msg = Text(width=40, height=4, wrap="word", yscrollcommand="true")
	msg.grid(row=0, column=1, padx=10, pady=5)

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

	C = Button(text="Send Message!", command=lambda: send(msg.get("1.0", 'end-1c'), recipient.get()))
	C.grid(row = 4, column = 0, rowspan = 2, pady=5, columnspan=2)

root = Tk()
login(root)
root.mainloop()