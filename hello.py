from flask import Flask
from flask import render_template
app = Flask(__name__, template_folder='templates')

# @app.route('/')
# def hello_world():
    # return 'Hello, World!'
	
@app.route('/')
def home(name=None):
    return render_template('index.html')