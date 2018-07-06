import json
from webscraper.webscraper import*
from flask import Flask
from flask import render_template, url_for
from flask import request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__, template_folder='templates')
app.config.from_pyfile('config.cfg')

mail = Mail(app)
s = URLSafeTimedSerializer("secrets")

with app.test_request_context('/searchresult', method='GET'):
   	assert request.path == '/searchresult'
   	assert request.method == 'GET'

with app.test_request_context('/confirmEmail', method='GET'):
   	assert request.path == '/confirmEmail'
   	assert request.method == 'GET'
	
@app.route('/')
def home():
	paths = ['events/ICMC','events/UFSCar', 'events/SESC']
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

# Manda um email de confirmação para o usuário
@app.route('/notification', methods=['GET'])
def notification():
	if request.method == 'GET':
		email = request.args.get('email', '')
		msg = Message('Confirm mail', sender="divulgasanca@gmail.com", recipients=[email])

		token = s.dumps(email, salt='email-confirm')
		link = url_for('confirmLink', token=token, _external=True)
		msg.body = 'Your link is {}'.format(link)

		registerUser(email,token, False)

		mail.send(msg)
		
		return 'Um email foi mandado no email especificado'

# Manda um email de confirmação para o usuário
@app.route('/confirmLink/<token>')
def confirmLink(token):
	try:
		email = s.loads(token, salt='email-confirm', max_age=3600)
	except SignatureExpired:
		return '<h1>The token is expired!</h1>'

	if confirmUser(email):
		return '<h1>Agora você receberá emails de notificação!</h1>'
	return 'Ocorreu algum erro'

@app.route('/notificateEvents', methods=['POST'])
def notificateEvents():
	if request.method == 'POST':
		email = request.args['emails']
		print(request.args['emails'])
		print(email)

		msg = Message('Novos eventos chegaram!', sender="divulgasanca@gmail.com", recipients=[email])
		msg.body = request.args['text']
		mail.send(msg)
	return 'OK'



if __name__ == '__main__':
	app.run(debug=True)