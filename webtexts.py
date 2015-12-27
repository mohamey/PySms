import vobject
from splinter import Browser
from selenium import webdriver

with Browser('phantomjs') as browser:
	fp = open('test.vcf', "r")
	content = fp.read()
	fp.close()

	vcards = vobject.readComponents(content)
	numbers = []
	for contact in vcards:
		#contact.prettyPrint()
		numbers.append(contact.tel.value)

#	for x in numbers:
#		print x

	url = "https://webtexts.three.ie"
	browser.visit(url)
	browser.fill('data[User][telephoneNo]', '0876477540')
	browser.fill('data[User][pin]', '940367')
	browser.find_by_css('a.trigger-submit').first.click()

	count = 0;
	while (count < len(numbers)):
		browser.fill('data[Message][message]', 'Automated Text Script Test')
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