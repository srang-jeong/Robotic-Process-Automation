'''
DataFrame이란?
DataFrame은 Pandas 라이브러리의 핵심 자료구조로, 
엑셀 표처럼 행(row)과 열(column)로 이루어진 2차원 테이블 형태의 데이터 구조입니다.

데이터구조: 배열(리스트), 딕셔너리(튜플)

특징
엑셀/CSV처럼 표 형식으로 데이터를 다룸
각 열은 시리즈(Series) 객체로 구성됨
행과 열에 인덱스(index) 를 지정할 수 있음
다양한 데이터타입(숫자, 문자열, 날짜 등) 혼합 가능
'''
import pandas as pd
# py -m pip install pandas

data = {
    "이름": ["홍길동", "김영희", "이철수"],
    "나이": [28, 34, 45],
    "직업": ["개발자", "디자이너", "데이터분석가"]
}

df = pd.DataFrame(data)
print("📊 === 기본 DataFrame ===")
print(df)
print()

print("🔢 === iloc (정수 위치 기반) ===")
print("첫 번째 행:", df.iloc[0])
print("첫 번째 행, 첫 번째 열:", df.iloc[0, 0])
print("첫 번째 행, 두 번째 열:", df.iloc[0, 1])
print("첫 번째 행, 세 번째 열:", df.iloc[0, 2])
print("처음 2행:\n", df.iloc[0:2])  # 0~1번째 행 (슬라이스는 끝 포함 X)
print()

print("🏷️ === loc (라벨 기반) ===")
print("인덱스 0인 행:", df.loc[0])
print("인덱스 0, '이름' 컬럼:", df.loc[0, '이름'])
print("인덱스 0, '나이' 컬럼:", df.loc[0, '나이'])
print("인덱스 0~1, '이름'과 '나이' 컬럼:\n", df.loc[0:1, ['이름', '나이']])
print()

print("📝 === 컬럼별 접근 ===")
print("이름 컬럼:", df['이름'])
print("나이 컬럼:", df['나이'])
print()


'''
주요 구조 용어
용어	설명
row	    가로 방향 데이터 (ex. 한 사람의 정보)
column	세로 방향 데이터 (ex. 이름, 나이, 직업)
index	각 행의 고유 번호 (기본값은 0부터 시작)
dtype	각 열의 데이터 타입
'''

print("🔍 === DataFrame 구조 정보 ===")
print("크기 (행, 열):", df.shape)         # (행 수, 열 수)
print("컬럼 목록:", df.columns.tolist())       # 열 이름 목록
print("인덱스 목록:", df.index.tolist())         # 인덱스 목록
print("데이터 타입:\n", df.dtypes)        # 열별 데이터 타입
print()
print("📋 === 전체 정보 요약 ===")
print(df.info())        # 전체 구조 요약