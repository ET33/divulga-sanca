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
	return result

# Posta um evento no firebase
def postFirebase(path, json):
	result = fb.post(path, json)

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
		
		# busca a data do evento  
		date = l.find_all('span')[1:3]
		# aplica um regex na data para retirar espaços e pulos de linha desnecessários
		for i in range(0, 2):
			date[i] = re.search(r'([\S].*[\S])', date[i].text).group()
		#junta as informações de dia com as informações de horário em uma string
		date_formated = date[0] + ' ' + date[1]

		#busca e formata a informação de endereço da imagem
		img = re.search(r'url\((.*)\)', children[4]['style']).group(1)

		data = {}
		data['title'] = children[3]['data-ga-action']
		data['date'] = date_formated
		data['tags'] = l.find('strong').text
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
			
# Busca os ventos pela data de inicio
def searchingForStartDate(key):
	
	# Lista dos eventos encontrados
	result = []
	
	# Buscando no ICMC
	result.extend(searchInDir('events/ICMC',key,'startDate'))
	
	# Buscando na Ufscar
	result.extend(searchInDir('events/UFSCar',key,'startDate'))
	
	for r in result:
		print(r['title'])

# Main
def main():
	deleteData('/events/')
	getICMC()
	getUFSCar()
	searchingForStartDate("25/07/2018")
	
if __name__ == '__main__':
	main()