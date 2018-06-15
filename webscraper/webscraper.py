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
def postFirebase(path, json):
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

		# pega o dicionário, e posta no firebase 
		postFirebase('/events', data)

# Main
def main():
	getICMC()
	getFirebase('/events')

if __name__ == '__main__':
	main()