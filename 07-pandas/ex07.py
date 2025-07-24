import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")

# 연도별 출간 도서 수
if '출간연도' in df.columns:
    year_counts = df['출간연도'].value_counts().sort_index()
    year_counts.plot(kind='line', marker='o') # 원모양
    plt.title('연도별 출간 도서 수')
    plt.xlabel('출간연도')
    plt.ylabel('도서 수')
    plt.tight_layout()
    plt.savefig('year_count.png')
    plt.show()

    # 연도별 평균 가격
    year_price = df.groupby('출간연도')['가격'].mean()
    year_price.plot(kind='line', marker='s', color='red') # s 정사각형
    plt.title('연도별 평균 도서 가격')
    plt.xlabel('출간연도')
    plt.ylabel('평균 가격')
    plt.tight_layout()
    plt.savefig('year_price.png')
    plt.show()
else:
    print('출간연도 컬럼이 없습니다.') 

# | 옵션    | 모양       | 의미            |
# | ----- | -------- | ------------- |
# | `'o'` | 원 ●      | 가장 흔하게 사용     |
# | `'s'` | 정사각형 ■   | square        |
# | `'^'` | 위쪽 삼각형 ▲ | triangle up   |
# | `'v'` | 아래 삼각형 ▼ | triangle down |
# | `'D'` | 마름모 ◆    | diamond       |
# | `'*'` | 별 ✱      | star          |
# | `'x'` | 엑스 ×     | cross         |
# | `'+'` | 플러스 +    | plus          |
