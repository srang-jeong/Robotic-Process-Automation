"""
구글 시트 읽기 - 가장 심플한 버전
"""

# py -m pip install gspread
# https://workspace.google.com/products/sheets/

import gspread
from google.oauth2.service_account import Credentials

# goole sheets API 활성화
# goole driver API 활성화
# 구글 시트 공유에 서비스 계정(이메일 추가)
# googlesheetpython@gspread-proj2.iam.gserviceaccount.com

# 구글 시트 API 스코프 설정
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# .gitignore에 confidencial.json 추가하여, 인증키 노출안되게 해야 됨!

# 구글 시트 API 인증
creds = Credentials.from_service_account_file("./09-excel/confidencial.json", scopes=scopes)
client = gspread.authorize(creds)

# 구글 시트 열기
sheet = client.open("성적표").sheet1

print("📊 구글 시트 내용:")
print("-" * 30)

# 모든 값 읽어서 출력
for row in sheet.get_all_values():
    # 빈 셀 제거
    filtered_row = []
    for cell in row:
        if cell.strip():  # 빈 문자열이 아니면
            filtered_row.append(cell)
    
    if filtered_row:  # 빈 행이 아니면 출력
        print(filtered_row) 