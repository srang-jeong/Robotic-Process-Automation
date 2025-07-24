import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

# 카테고리/저자별 평균 가격 피벗테이블
pivot = pd.pivot_table(df, index='카테고리', columns='저자', values='가격', aggfunc='mean', fill_value=0)

# 0 ~ 1 정규화 : 35000 - 17000 => 1 ~ 0
pivot_norm = (pivot - pivot.min().min()) / (pivot.max().max() - pivot.min().min())

plt.figure(figsize=(10,6))
sns.heatmap(pivot_norm, annot=True, fmt='.2f', cmap='YlGnBu')
plt.title('카테고리/저자별 평균 가격 (정규화) Heatmap')
plt.xlabel('저자')
plt.ylabel('카테고리')
plt.tight_layout()
plt.savefig('category_author_price_heatmap.png')
plt.show() 