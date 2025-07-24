"""
openpyxl로 엑셀 파일 읽기 - 가장 심플한 버전
"""

import openpyxl

# 엑셀 파일 열기
workbook = openpyxl.load_workbook('./09-excel/성적표.xlsx')

# 활성 시트 가져오기
sheet = workbook.active

print("📊 성적표 내용:")
print("-" * 30)

# 모든 셀 읽어서 출력
for row in sheet.iter_rows(values_only=True):
    # None이 아닌 값들만 필터링(리스트 컴프리헨션 (한 줄로 압축))
    filtered_row = []
    for cell in row:
        if cell is not None:
            filtered_row.append(cell)
    # filtered_row = [cell for cell in row if cell is not None]
    if filtered_row:  # 빈 행이 아니면 출력
        print(filtered_row)

# 워크북 닫기
workbook.close()
