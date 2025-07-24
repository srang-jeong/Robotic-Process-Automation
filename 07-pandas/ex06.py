import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

# 저자별 도서 수 barplot
author_counts = df['저자'].value_counts()
author_counts.plot(kind='bar', color='lightgreen')
plt.title('저자별 도서 수')
plt.xlabel('저자')
plt.ylabel('도서 수')
plt.tight_layout()
plt.savefig('author_count.png')
plt.show()


# 가격 boxplot
plt.figure()
df.boxplot(column='가격')
plt.title('도서 가격 Boxplot')
plt.ylabel('가격')
plt.tight_layout()
plt.savefig('price_boxplot.png')
plt.show() 

# 중앙선 (검정선): 도서 가격의 중앙값 (Median).
# 상자(Box): 전체 도서 가격 중에서 Q1 (25%) ~ Q3 (75%) 구간을 의미.
# 상자의 아래 경계 (Q1): 약 19,000원
# 상자의 위 경계 (Q3): 약 27,000원
# 상자 내부의 중앙선: 약 22,500원 → 중앙값
# 수염(Whiskers):
# 아래쪽: 약 17,000원
# 위쪽: 약 35,000원
# 이상치 없음: Boxplot 외부에 점들이 없는 것으로 보아, 특이하게 비싼/싼 책은 없음.