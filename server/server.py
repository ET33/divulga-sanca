import forms
import json 
from webscraper.webscraper import*
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__, template_folder='templates')

	
@app.route('/')
def home():
	events = getFirebase('/events/ICMC')
	allEvents = []

	for i in events:
		allEvents.append(events[i])

	events = getFirebase('/events/UFSCar')
	
	for i in events:
		allEvents.append(events[i])
	
    
	return render_template('index.html', cards=allEvents)
	

with app.test_request_context('/searchresult', method='GET'):
    assert request.path == '/searchresult'
    assert request.method == 'GET'
	
	
@app.route('/searchresult', methods=['GET'])
def search():
	if request.method == 'GET':
		search = request.args.get('search', '')
	else:
		search = 'erro'
	
	
	# events = getFirebase('/events/ICMC')
	# allEvents = []
		
	# for i in events:
		# if search in events[i]:
			# allEvents.append(events[i])

	# events = getFirebase('/events/UFSCar')
	
	# for i in events:
		# if search in events[i]:
			# allEvents.append(events[i])
	
	return search
	


if __name__ == '__main__':
	app.run(debug=True)