import json 
import requests
from webscraper import*

def sendEmails(newEvents):
	if len(newEvents) > 0:
		emailText = str(len(newEvents)) + " novos eventos chegaram!\n"
		for j in newEvents:
			emailText += ("*" + str(j['title']) + "\n")
		print(emailText)
		
		allEmails = []
		emails = getFirebase('emails')
		for j in emails:
			if emails[j]['status'] == True:
				allEmails.append(emails[j]['email'])

		# TODO: trocar host para domínio
		r = requests.post("localhost:5000/notificateEvents", data=allEmails)

if __name__ == '__main__':
	app.run(debug=True)