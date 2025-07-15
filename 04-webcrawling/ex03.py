import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/04-webcrawling/test1.html"

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
print(soup.find('h1').text)