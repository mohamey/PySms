from Tkinter import *
from splinter import Browser
import tkMessageBox
import time

loggedin = False;
browser = Browser('phantomjs')

def initialise(frame):
	phoneString = ""
	passString = ""
	phoneFrame = Frame(frame)
	phoneFrame.pack()
	passwordFrame = Frame()
	passwordFrame.pack()

	PNLabel = Label(phoneFrame,text="Phone number")
	PNLabel.pack(side = LEFT)
	PhoneNumber = Entry(phoneFrame, textvariable=phoneString)
	PhoneNumber.pack(side=RIGHT)
	PassLabel = Label(passwordFrame, text="Password")
	PassLabel.pack(side = LEFT)
	Password = Entry(passwordFrame, show="*", textvariable=passString)
	Password.pack(side = RIGHT)

	def failed():
		print "Sorry, you entered an invalid phone number/password"
		tkMessageBox.showinfo("Oh No :O", "You have entered an invalid phone number/password")

	def login(phone, password):
		url = "https://webtexts.three.ie"
		browser.visit(url)
		browser.fill('data[User][telephoneNo]', phone)
		browser.fill('data[User][pin]', password)
		browser.find_by_css('a.trigger-submit').first.click()
		print browser.url
		if browser.url == "https://webtexts.three.ie/":
			failed()
		else:
			phoneFrame.destroy()
			passwordFrame.destroy()
			B.destroy()
			print "Frames Destroyed"
			sendMessage(root)


	B = Button(text="login", command= lambda: login(PhoneNumber.get(), Password.get()))
	B.pack()

def sendMessage(frame):
	print "Entered send message"
	messageFrame = Frame(frame)
	messageFrame.pack()
	recipientFrame = Frame()
	recipientFrame.pack()

	msgLabel = Label(messageFrame, text="Message")
	msgLabel.pack(side = LEFT)
	msg = Entry(messageFrame)
	msg.pack(side = RIGHT)

	recipientLabel = Label(recipientFrame, text="Recipient")
	recipientLabel.pack(side = LEFT)
	recipient = Entry(recipientFrame)
	recipient.pack(side = RIGHT)

	def send(message, recipient):
		browser.fill('data[Message][message]', message)
		browser.fill('data[Message][recipients_individual][0]', recipient)
		browser.find_by_css('a.trigger-submit').first.click()

	C = Button(text="Send!", command=lambda: send(msg.get(), recipient.get()))
	C.pack()

root = Tk()
initialise(root)
root.mainloop()