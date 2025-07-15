import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/04-webcrawling/test2.html"

html = requests.get(url).text

# HTML 파싱(분석,추출)
soup = BeautifulSoup(html, 'html.parser')

# 태그 접근 방법
print(soup.title)
print(soup.title.text)

print(soup.h1['id'])
print(soup.h1.text)

print(soup.p['class']) # 사용 X
print(soup.p['class'][0])
print(soup.p.text)

print(soup.find_all('p')[0].text)
print(soup.find_all('p')[1].text)
print(soup.find_all('a')[0]['href'])
print(soup.find_all('a')[1]['href'])

print(soup.find('p')) # 첫번째 p만
print(soup.find_all('p')) # 리스트 p만
print(soup.find('p', class_='content'))
print(soup.find('h1', id='title'))

