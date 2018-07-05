from webscraper.webscraper import* 
from flask import Flask,render_template

app = Flask(__name__,template_folder='templates')


@app.route('/home')
def home(): 
	events = getFirebase('/events/ICMC')
	allEvents = []

	for i in events:
		allEvents.append(events[i])

	events = getFirebase('/events/UFSCar')
	
	for i in events:
		allEvents.append(events[i])

	return render_template('home.html', posts=allEvents)

if __name__ == '__main__':
	app.run(debug=True)
