import requests					# load no site
from bs4 import BeautifulSoup	# Para processar o html
import json 					# Montar o obj. JSON
import re 						# Regex em Python
from firebase import firebase   # firebase da biblioteca python-firebase

# Conecta com o firebase configurado
fb = firebase.FirebaseApplication('https://eng-soft-f1c51.firebaseio.com', None)


# Pega os eventos contidos no nó 'path' do firebase
def getFirebase(path):
	result = fb.get(path, None)
	print(result)

# Posta um evento no firebase
def postFirebase(json, path):
	user = 'admin'
	result = fb.post(path, json)
	print(result)

# Carrega uma página e retorna uma estrutura navegável do bs4
def load(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup

# Pega as tags contidas nos links dos eventos próprios do ICMC
def getMoreInfo(url, data, _class):
	soup = load(url)
	links = soup.select(_class)
	line = links[0].get_text()
	res = re.sub(r'\s+', ' ', line ).strip()	
	data['tags'].append(res)

#Pega informações do site da UFSCar
def getUFSCar():
	url = 'https://www2.ufscar.br/eventos'
	soup = load(url)
	
	#Faz uma lista de todos os eventos do HTML do site
	links = soup.select('tr')
	ll = list(links)
	
	#Para todos os eventos listados...
	for l in ll:
		children = l.findChildren()
		
		#Pegar data e nome do evento
		data = {}
		data['date'] = children[0].get_text()
		print("date: " + data['date'])
		data['title'] = children[1].get_text()
		print("title: " + data['title'])
		data['tags'] = ['UFSCar', 'Eventos']
		
		#Dentre as informações contidas em a...
		a = l.find('a')		
		#pegar o href que contem o link
		data['href'] = a.get('href')
		
		print("link: " + data['href'])
		
		# pega o dicionário, transforma em um JSON e posta no firebase 
		json_data = json.dumps(data)
		print(json_data + '\n')
		postFirebase(json_data, '/events')
		
		
	
# Pega as informações do site do ICMC
def getICMC():
	url = 'https://www.icmc.usp.br/eventos'
	soup = load(url)

	# Seleciona o HTML aonde está os dados do evento e transforma em uma lista
	links = soup.select('.bloco a')
	ll = list(links)

	#percorre a lista e monta um dicionário de cada um dos eventos
	for l in ll:
		children = l.findChildren()

		data = {}
		data['title'] = children[2].get_text()
		data['date'] = children[3].get_text()
		data['tags'] = ['ICMC', 'Eventos']
		data['img'] =  'https://www.icmc.usp.br' + children[0]['src']

		# Configura o link do evento
		if l['href'][0] == '/':	# Link Interno
			data['href'] = 'https://www.icmc.usp.br' + l['href']
			getMoreInfo(data['href'], data, '.caixa-noticia-categoria')
		else :					# Link Externo
			data['href'] = l['href']

		# pega o dicionário, transforma em um JSON e posta no firebase 
		json_data = json.dumps(data)
		print(json_data)
		postFirebase(json_data, '/events')

# Main
def main():
	getUFSCar()
	getICMC()
	getFirebase('/events')

if __name__ == '__main__':
	main()