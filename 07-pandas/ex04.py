import pandas as pd
import matplotlib.pyplot as plt

# py -m pip install matplotlib(맷트롯립)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books.csv")

grouped = df.groupby("카테고리")["가격"].mean()

# 카테고리별 평균 가격 시각화
grouped.plot(kind="bar") # 막대 차트
plt.title("카테고리별 평균 가격")
plt.xlabel("카테고리")
plt.ylabel("가격")
plt.tight_layout()  # 타이트하게 여백을 맞춤.

# 시각화 파일로 저장 (show() 전에 해야 함!)
plt.savefig("report.png")

plt.show()

# CSV → HTML 자동 리포트 저장 예시
df.to_html("report.html")

