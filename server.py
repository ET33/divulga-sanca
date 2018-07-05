from flask import Flask
from flask import render_template
app = Flask(__name__, template_folder='templates')

	
@app.route('/')
def home(name=None):

	cards = []
    
	return render_template('index.html', cards=['1', '2', '3', '4', '1'])