import requests					# load no site
from bs4 import BeautifulSoup	# Para processar o html
import json 					# Montar o obj. JSON
import re 						# Regex em Python
from firebase import firebase   # firebase da biblioteca python-firebase
import datetime
import unicodedata

# Conecta com o firebase configurado
fb = firebase.FirebaseApplication('https://eng-soft-f1c51.firebaseio.com', None)
#Normalize uma string num formato padrão para ajudar nas comparações de buscas
def normalizeCaseless(text):
	return unicodedata.normalize("NFKD", text.casefold())
# Pega os eventos contidos no nó 'path' do firebase
def getFirebase(path):
	result = fb.get(path, None)
	return result

# Posta um evento no firebase
def postFirebase(path, json):
	treated_title = re.sub(r'[/]', '_', json['title'])
	result = fb.patch(path + '/' + treated_title, json)

def postUsers(path, json):
	treated_email = re.sub(r'[\.]', '_', json['email'])
	result = fb.patch(path + '/' + treated_email, json)

# Carrega uma página e retorna uma estrutura navegável do bs4
def load(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup

# Pega as tags contidas nos links dos eventos próprios do ICMC
def getMoreInfoICMC(url, data, _class):
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
		#Pega a string da data
		dateString =  re.findall(r'(\d{1,2}\/\d{1,2}\/\d{2,4})',children[0].get_text()) 
		#Pega a data de início
		data['startDate'] = dateString[0]
		#Se tiver data de fim pegue, senão deixa vazio
		if(len(dateString) > 1):
			data['endDate'] = dateString[1]
		else:
			data['endDate'] = ""
			
		data['title'] = children[1].get_text()
		data['tags'] = ['UFSCar', 'Eventos']
		# Coloca a imagem do logo da ufscar para o dado
		data['img'] = "http://tecnologiademateriais.com.br/portaltm/wp-content/uploads/2018/02/logo_ufscar.png"
		#Dentre as informações contidas em a...
		a = l.find('a')		
		#pegar o href que contem o link
		data['href'] = a.get('href')
		
		# pega o dicionário, transforma em um JSON e posta no firebase 
		postFirebase('/events/UFSCar', data)
		
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
		#Pega a string da data
		dateString = re.findall(r'(\d{1,2}\/\d{1,2}\/\d{2,4})',children[3].get_text()) 
		#Pega a data de início
		data['startDate'] = dateString[0]
		#Se tiver data de fim pegue, senão deixa vazio
		if(len(dateString) > 1):
			data['endDate'] = dateString[1]
		else:
			data['endDate'] = ""
		data['title'] = children[2].get_text()
		data['tags'] = ['ICMC', 'Eventos']
		data['img'] =  'https://www.icmc.usp.br' + children[0]['src']

		# Configura o link do evento
		if l['href'][0] == '/':	# Link Interno
			data['href'] = 'https://www.icmc.usp.br' + l['href']
			getMoreInfoICMC(data['href'], data, '.caixa-noticia-categoria')
		else :					# Link Externo
			data['href'] = l['href']
			
		postFirebase('/events/ICMC', data)


def getSESC():
	url = 'https://www.sescsp.org.br/unidades/ajax/agenda-filtro.action?id=21&maxResults=1000'
	soup = load(url)

	# Seleciona o HTML aonde está os dados do evento e transforma em uma lista
	links = soup.select('.block_agenda')
	ll = list(links)

	#percorre a lista e monta um dicionário de cada um dos eventos
	for l in ll:
		children = l.findChildren()
		
		# pega a informação de data no HTML
		date = l.find('div', {"class": "line-infos line-infos-list"}).find('span').text

		# aplica um regex na data para encontrar a data de início e possível fim do evento
		date_regex = re.findall(r'../..', date)
		
		#busca e formata a informação de endereço da imagem
		img = re.search(r'url\((.*)\)', children[4]['style']).group(1)

		data = {}
		data['title'] = children[3]['data-ga-action']
		data['startDate'] = date_regex[0] + "/" + str(datetime.datetime.now().year)	
		if len(date_regex) > 1: 
			data['endDate'] = date_regex[1] + "/" + str(datetime.datetime.now().year)
		data['tags'] = [l.find('strong').text]
		data['img'] =  'https://www.sescsp.org.br' + img
		data['href'] = 'https://www.sescsp.org.br' + l.find('a', {'class' :'desc'})['href']

		postFirebase('/events/SESC', data)
		

def deleteData(path):
	result = fb.delete(path, None)

# Busca dentro de um diretorio de eventos
def searchInDir(path, key, tag):
	
	events = getFirebase(path)
	result = []
	
	for i in events:
		if(events[i][tag] == key):
			result.append(events[i])
	return result
			
# Busca os eventos pela data de inicio
def searchForStartDate(key):
	
	# Lista dos eventos encontrados
	result = []
	#define os diretórios de busca
	paths = ['events/ICMC','events/UFSCar','events/SESC']
	
	for i  in paths:
		result.extend(searchInDir(i,key,'startDate'))

	return result
	
# Busca eventos pelo título
def searchForTitle(key):
	
	#lista dos eventos encontrados
	result = []
	#define os diretórios de busca
	paths = ['events/ICMC','events/UFSCar', 'events/SESC']
	
	#busca nos diretorios definidos
	for i in paths:
		events = getFirebase(i)
		for j in events:
			title = events[j]['title']
			if normalizeCaseless(key) in normalizeCaseless(title):
				result.append(events[j])

	return result

# Cadastra o usuario na lista dos interressados
def registerUser(email, key, status):
	data = {
		'email': email,
		'key': key,
		'status': status
	}

	postUsers('/users', data)

def confirmUser(email):
	us = getFirebase('users/')

	for i in us:
		if(email == i['key']):
			i['status'] = True
# Main
def main():
	#deleteData('/events/')
	getICMC()
	getUFSCar()
	getSESC()
	#searchForStartDate("25/07/2018")
	#searchForTitle("BIOLOGIA")

if __name__ == '__main__':
	main()