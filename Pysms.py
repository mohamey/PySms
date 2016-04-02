import vobject
from tkinter import *
from tkinter import messagebox
import keyring
import dependencies.three as three
import pickle
import os
import sys

##Destroy the frames in a grid
def destroyGrid(frame):
	for widget in frame.grid_slaves():
		widget.destroy()

##Save login Details
def saveLogin(login):
	try:
		fileObject = open("userData.txt", "wb")
		keyring.set_password("Pysms", login[0], login[1])
		pickle.dump(login[0], fileObject, protocol=pickle.HIGHEST_PROTOCOL)
		fileObject.close()
	except Exception as e:
		print("Failed to save login\n")
		print(sys.exec_info()[0])

##Purge login details if user no longer wants it saved
def purgeLogin(number):
	try:
		keyring.delete_password("Pysms", number)
		os.remove("userData.txt")
	except Exception as e:
		print("Error, unable to purge login details")
		print(sys.exec_info()[0])

##Check if login details are already present
def checkLogin():
	try:
		fileObject = open("userData.txt", 'rb')
		loginDetails = pickle.load(fileObject)
		if loginDetails:
			return [loginDetails, keyring.get_password("Pysms", loginDetails)]
		return loginDetails
	except:
		print("Error checking for login details")

##Process Login Details
def processLogin(phoneNumber, password, saveDetails, retrieved, frame):
	loginDetails = [phoneNumber, password]
	if three.login(loginDetails):
		if saveDetails:
			saveLogin(loginDetails)
		elif retrieved:
			purgeLogin(phoneNumber)
		destroyGrid(frame)
		sendMessage(frame)
	else:
		messagebox.showerror("Unable to login", "Please check your username/password combination and try again")

##Generate a login window
def generateLogin(frame):
	frame.wm_title("Pysms")

	##Retrieve stored info if available
	loginNumber = loginPassword = ""
	saveDetails = BooleanVar()
	storedDetails = checkLogin()
	retrieved = False

	if storedDetails:
		loginNumber = storedDetails[0]
		loginPassword = storedDetails[1]
		saveDetails.set(True)
		retrieved = True
	else:
		saveDetails.set(False)

	##Set tkinter gui
	phoneLabel = Label(text="Phone Number")
	phoneLabel.grid(row=0, column=0, sticky="W")

	phoneEntry = Entry(frame)
	phoneEntry.insert(END, loginNumber)
	phoneEntry.grid(row=0, column=1, padx=5, pady=5)

	passLabel = Label(text="Password")
	passLabel.grid(row=1, column=0, sticky="W")

	passEntry = Entry(frame, show="*")
	passEntry.insert(END, loginPassword)
	passEntry.grid(row=1, column=1, padx=5, pady=5)

	checkSave = Checkbutton(text="Save my login details", variable=saveDetails, onvalue=True, offvalue=False)
	checkSave.grid(row=2, column=0, columnspan=2, pady=5)

	loginButton = Button(text="login", command=lambda: processLogin(phoneEntry.get(), passEntry.get(), saveDetails.get(), retrieved, frame))
	loginButton.grid(row=3, column=0, columnspan=2, pady=5)


###Methods below this line are used for sending messages #####


##Generate the send message window
def sendMessage(frame):
	##Process message before sending
	def processSend(msg, recipient):
		msgToSend = msg.strip()
		messageSize = (len(msgToSend)/160)+1
		totalMessages = len(numbers) * messageSize
		if(int(remainingTexts) > totalMessages):
			numbers.append(recipient)
			if three.send(msgToSend, numbers):
				messagebox.showinfo("Success", "Message was successfully sent")
				destroyGrid(frame)
				sendMessage(frame)
			else:
				messagebox.showinfo("Error", "An error occurred while sending your message. Please try again later")
		else:
			messagebox.showerror("Error", "You do not have enough remaining web texts to send "+str(totalMessages)+" messages")

	##Update message length
	def update(event):
		if event.keycode == 8:
			message = msg.get("1.0", "end-1c")
			charCounter.set("Character Count: "+str(len(msg.get("1.0", "end-2c"))))
		else:
			charCounter.set("Character Count: "+str(len(msg.get("1.0", "end"))))

	def browseVcard(browseButton):
		from tkinter import filedialog
		vcard = filedialog.askopenfilename(filetypes=[("Vcards", "*.vcf")])
		display = str(vcard).split('/')
		browseButton.set(display[-1])
		fp = open(vcard, "r")
		content = fp.read()
		fp.close()

		vcards = vobject.readComponents(content)
		for contact in vcards:
			try:
				numbers.append(contact.tel.value)
			except:
				pass

	frame.wm_title("Send Message")

	numbers = []
	remainingTexts = -1
	try:
		remainingTexts = three.retrieveRemaining()
	except:
		print("Failed to retrieve remaining webtexts")

	###Set tkinter send message gui
	msgLabel = Label(text="Message")
	msgLabel.grid(row=0, column=0, sticky="W", padx=10)
	msg = Text(width=40, height=4, wrap="word", yscrollcommand="true")
	msg.grid(row=0, column=1, padx=10, pady=5)

	remainingLabel = Label(text="Remaining Webtexts: "+str(remainingTexts))
	remainingLabel.grid(row=1, column=0, padx= 5, sticky="E")

	charCounter = StringVar()
	charCounter.set("Character Count: 0")
	msg.bind("<Key>", update)
	charcount = Label(textvariable=charCounter)
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
