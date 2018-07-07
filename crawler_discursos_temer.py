import requests
from bs4 import BeautifulSoup

URL_BASE = 'http://www.itamaraty.gov.br'

URL_INICIAL = 'http://www.itamaraty.gov.br/pt-BR/discursos-artigos-e-entrevistas-categoria/presidente-da-republica-federativa-do-brasil-discursos?limitstart='

def get_urls(soup):
    h2_list = soup.find_all('h2', attrs={"class":"tileHeadline"})
    urls = [URL_BASE + h2.a['href'] for h2 in h2_list]
    return urls

def get_michel(url_list):
    # identifica apenas discursos do Michel Temer
    michel_discurs = [item for item in url_list if item.find('michel') != -1]
    return michel_discurs

def get_url_discourse(url):
    url_list = []
    for i in range(4):
        url_page = url + str(i)
        r = requests.get(url_page)
        soup = BeautifulSoup(r.content, "html.parser")
        url_list += get_urls(soup)
        r.close()
    return get_michel(url_list) # apenas discurso do Michel Temer

def get_discourse_text(soup):
    text = ' '.join([item.text for item in soup.find('div', {'id': 'content'}).findAll('p')])
    return text

def main():
	lista_urls = get_url_discourse(URL_INICIAL)
	file = open('texto_discursos.txt', 'w')
	for url in lista_urls:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		discourse_text = get_discourse_text(soup)
		file.write('%s\n' %discourse_text)
	file.close()

if __name__=='__main__':
	main()