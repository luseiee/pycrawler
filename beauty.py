import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers=headers)

Soup = BeautifulSoup(start_html.text,'lxml')
all_a = Soup.find('div', class_='all').find_all('a')
cwd = os.getcwd()
for a in all_a:
	title = a.get_text()
	path = str(title).strip()
	os.makedirs(os.path.join(cwd, 'mzitu', path))
	os.chdir(os.path.join(cwd, 'mzitu', path))
	href = a['href']
	html = requests.get(href, headers=headers)
	html_Soup = BeautifulSoup(html.text, 'lxml')
	max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
	for page in range(1, int(max_span) + 1):
		page_url = href + '/' + str(page)
		img_html = requests.get(page_url, 'lxml')
		img_Soup = BeautifulSoup(img_html.text, 'lxml')
		img_url = img_Soup.find('div', class_='main-image').find('img')['src']
		name = img_url[-9:-4]
		img = requests.get(img_url, headers=headers)
		f = open(name+'.jpg', 'ab')
		f.write(img.content)
		f.close()


