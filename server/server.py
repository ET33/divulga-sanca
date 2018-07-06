import smtplib
import json 
from webscraper.webscraper import*
from flask import Flask
from flask import render_template
from flask import request
from firebase import firebase
import datetime
import unicodedata
import re

app = Flask(__name__, template_folder='templates')

with app.test_request_context('/searchresult', method='GET'):
   	assert request.path == '/searchresult'
   	assert request.method == 'GET'
	
@app.route('/')
def home():
	paths = ['/events/ICMC','/events/UFSCar','events/SESC']
	allEvents = []

	for i in paths:
		events = getFirebase(i)
		for j in events:
			allEvents.append(events[j])

	return render_template('index.html', cards=allEvents)

@app.route('/searchresult', methods=['GET'])
def search():
	if request.method == 'GET':
		key = request.args.get('search', '')
		result = searchForTitle(key)
		if(len(result) > 0):
			return render_template('index.html', cards=result)
		else:
			response = "Nenhum resultado encontrado pela chave: " + key + ". Tente mais uma vez."
			return response

# @app.route('/googlesearch', methods=['GET'])
# def gSearch():
	# if request.method == 'GET':
		# title = request.args.get('titulo', '')
		# date = request.args.get('data', '')
		
	# return title
	
@app.route('/notification', methods=['GET'])
def notification():
	
	email = request.args.get('email', '')
	
	return email

	
if __name__ == '__main__':
	app.run(debug=True)