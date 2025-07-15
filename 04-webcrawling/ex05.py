import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# select : css선택자를 사용함.
# .titleline > a : 클래스이름 titleline의 바로 밑의 a태그를 선택하라.
titles = soup.select('.titleline > a')
print(titles)
print()

for i, title in enumerate(titles[:5], 1):
    print(f"{i}, {title.text} ({title['href']})")