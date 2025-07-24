import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

plt.figure(figsize=(8,5))
sns.boxplot(x='저자', y='가격', data=df, showfliers=False)
sns.swarmplot(x='저자', y='가격', data=df, color='black', size=6)
plt.title('저자별 가격 분포 (Boxplot + Swarmplot)')
plt.tight_layout()
plt.savefig('box_swarmplot.png')
plt.show() 