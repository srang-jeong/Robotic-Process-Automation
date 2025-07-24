import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

# 카테고리/저자별 평균 가격 계산
pivot = pd.pivot_table(df, index='카테고리', columns='저자', values='가격', aggfunc='mean', fill_value=0)

# 막대그래프(Bar plot)로 시각화
pivot.plot(kind='bar', figsize=(10,6))
plt.title('카테고리/저자별 평균 가격 (Bar plot)')
plt.xlabel('카테고리')
plt.ylabel('평균 가격')
plt.legend(title='저자')
plt.tight_layout()
plt.savefig('matplotlib_category_author_price_bar.png')
plt.show()
