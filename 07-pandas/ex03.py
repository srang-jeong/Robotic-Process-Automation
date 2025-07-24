import pandas as pd

df = pd.read_csv("./07-pandas/books.csv")

# # 평균, 최대값 등 통계
# print(df.describe())

# 그룹별 통계
grouped = df.groupby("카테고리")["가격"].std()
print(grouped)

# 정렬
# df = df.sort_values(by="가격", ascending=True)
# print(df)

# 평균과 표준편차 정리
# 함수	    의미	    알 수 있는 것	    예시
# mean()	평균값	    그룹의 중심값	    AI 도서 평균: 39,000원
# std()	    표준편차	그룹의 분산 정도	AI 도서 편차: 1,000원 (일정함)

# 표준편차가 작으면 → 데이터가 평균 주변에 모여있음 (일정함)
# 표준편차가 크면 → 데이터가 평균에서 많이 흩어져있음 (다양함)