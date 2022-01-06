import yagmail

def sendEmail():
	yag = yagmail.SMTP('hextech.firrj@gmail.com', 'Mariogotze9')
	contents = [
    "unknow face detected"
	]
	yag.send('firasjaberc@gmail.com', 'Unknown face detected', contents)


