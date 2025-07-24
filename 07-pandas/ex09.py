import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# py -m pip install seaborn

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

plt.figure(figsize=(8,5))
sns.violinplot(x='카테고리', y='가격', data=df)
plt.title('카테고리별 가격 분포 (Violinplot)')
plt.tight_layout()
plt.savefig('violinplot.png')
plt.show() 