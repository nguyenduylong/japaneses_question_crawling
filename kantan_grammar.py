from bs4 import BeautifulSoup
import requests


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


crawl_url = 'https://kantan.vn//grammar-20.htm'

page = requests.get(crawl_url, headers=HEADERS)
soup = BeautifulSoup(page.content, 'html.parser')
detail_popup = soup.find('div', class_='dekiru-popup-detail')

if detail_popup is not None:
    print(detail_popup.find('div', class_='GrammarDetail'))
