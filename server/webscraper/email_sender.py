import json 
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
			print("enviar email para : " + emails[j]['email'])


if __name__ == '__main__':
	app.run(debug=True)