# ex08.py
# https://www.hankyung.com/globalmarket/news-globalmarket
# 한경글로벌 마켓의 뉴스 기사 타이틀 10개 / image url을 출력하시오.

import requests
from bs4 import BeautifulSoup

url = "https://www.hankyung.com/globalmarket/news-globalmarket"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

results = []
for li in soup.select("#contents > ul > li")[:10]:
    # 타이틀 추출
    title_tag = li.select_one("div > div > h2")
    title = title_tag.get_text(strip=True) if title_tag else None
    # 이미지 URL 추출 (질문에서 제공한 셀렉터 기준)
    img_tag = li.select_one("div > figure > a > img")
    img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None
    results.append((title, img_url))

# 결과 출력
for idx, (title, img_url) in enumerate(results, 1):
    print(f"{idx}. {title} / {img_url}")