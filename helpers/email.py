import yagmail

def sendEmail(filename):
	yag = yagmail.SMTP('hextech.firrj@gmail.com', 'Mariogotze9')
	contents = [
    "unknow face detected :",
		"uploaded picture : "+filename
	]
	yag.send('firasjaberc@gmail.com', 'Unknown face detected', contents)


