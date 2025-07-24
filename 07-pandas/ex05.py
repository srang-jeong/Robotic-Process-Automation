import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

# 카테고리별 도서 수 시각화
category_counts = df['카테고리'].value_counts()
category_counts.plot(kind='bar', color='skyblue')
plt.title('카테고리별 도서 수')
plt.xlabel('카테고리')
plt.ylabel('도서 수')
plt.tight_layout()
plt.savefig('category_count.png')
plt.show()

# 가격 분포 히스토그램
plt.figure()
df['가격'].plot(kind='hist', bins=10, color='orange', edgecolor='black')
plt.title('도서 가격 분포')
plt.xlabel('가격')
plt.ylabel('도서 수')
plt.tight_layout()
plt.savefig('price_hist.png')
plt.show() 