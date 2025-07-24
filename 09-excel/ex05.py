"""
구글 시트 성적표 읽기 + 평균 점수와 최대 득점자 계산하여 맨 아래 행에 추가
ex03.py의 구글 시트 버전
"""

import gspread
from google.oauth2.service_account import Credentials

# 구글 시트 API 스코프 설정
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# 구글 시트 API 인증
creds = Credentials.from_service_account_file("./09-excel/confidencial.json", scopes=scopes)
client = gspread.authorize(creds)

# 구글 시트 열기 (본인의 구글 시트 URL로 변경하세요)
sheet_url = "https://docs.google.com/spreadsheets/d/10dAE9fJ9ZSZXGXO7mhYTkDQoHq0mqFpgZdVzb4tUwqI/edit"
try:
    sheet = client.open_by_url(sheet_url).sheet1
    use_real_sheet = True
except:
    # 실제 시트 연결이 안 되면 시뮬레이션 모드
    use_real_sheet = False
    print("⚠️  실제 구글 시트 URL을 설정하지 않았습니다.")
    print("📊 시뮬레이션 모드로 진행합니다.")

print("📊 원본 성적표:")
print("-" * 50)

# 성적 데이터를 저장할 리스트
students = []  # 학생 데이터

if use_real_sheet:
    # 실제 구글 시트에서 데이터 읽기
    all_values = sheet.get_all_values()
    
    for row_num, row in enumerate(all_values, 1):
        # 빈 셀 제거
        filtered_row = []
        for cell in row:
            if cell.strip():
                filtered_row.append(cell)
        
        if filtered_row:
            print(filtered_row)
            
            # 헤더가 아닌 학생 데이터면 저장
            if row_num > 1 and len(filtered_row) >= 5:
                try:
                    student_data = {
                        '번호': int(filtered_row[0]),
                        '이름': filtered_row[1],
                        '국어': int(filtered_row[2]),
                        '영어': int(filtered_row[3]),
                        '수학': int(filtered_row[4])
                    }
                    students.append(student_data)
                except ValueError:
                    # 숫자가 아닌 경우 건너뛰기
                    continue
else:
    # 시뮬레이션 데이터
    sample_data = [
        ['번호', '이름', '국어', '영어', '수학'],
        ['1', '홍길동', '80', '70', '60'],
        ['2', '변사또', '90', '90', '80'],
        ['3', '사임당', '70', '80', '100']
    ]
    
    for row_num, row in enumerate(sample_data, 1):
        print(row)
        
        # 헤더가 아닌 학생 데이터면 저장
        if row_num > 1:
            student_data = {
                '번호': int(row[0]),
                '이름': row[1],
                '국어': int(row[2]),
                '영어': int(row[3]),
                '수학': int(row[4])
            }
            students.append(student_data)

print("\n" + "="*50)
print("📈 계산 결과:")
print("="*50)

# 1. 과목별 평균 계산
korean_sum = sum(student['국어'] for student in students)
english_sum = sum(student['영어'] for student in students)
math_sum = sum(student['수학'] for student in students)
student_count = len(students)

korean_avg = korean_sum / student_count
english_avg = english_sum / student_count
math_avg = math_sum / student_count

print(f"📊 과목별 평균:")
print(f"   국어 평균: {korean_avg:.1f}점")
print(f"   영어 평균: {english_avg:.1f}점")
print(f"   수학 평균: {math_avg:.1f}점")

# 2. 최대 득점자 찾기
max_score = 0
top_student = ""

print(f"\n🎯 개별 총점:")
for student in students:
    total = student['국어'] + student['영어'] + student['수학']
    print(f"   {student['이름']}: {total}점")
    
    if total > max_score:
        max_score = total
        top_student = student['이름']

print(f"\n🏆 최대 득점자: {top_student} ({max_score}점)")

# 3. 구글 시트에 결과 추가
print(f"\n📝 구글 시트에 결과 추가중...")

if use_real_sheet:
    try:
        # 현재 마지막 행 찾기
        all_values = sheet.get_all_values()
        last_row = len(all_values)
        
        # 평균 점수 행 추가
        avg_row = last_row + 2  # 한 줄 띄우고 추가
        sheet.update_cell(avg_row, 1, "평균")
        sheet.update_cell(avg_row, 2, "")
        sheet.update_cell(avg_row, 3, round(korean_avg, 1))
        sheet.update_cell(avg_row, 4, round(english_avg, 1))
        sheet.update_cell(avg_row, 5, round(math_avg, 1))
        
        # 최대 득점자 행 추가
        top_row = avg_row + 1
        sheet.update_cell(top_row, 1, "최고점")
        sheet.update_cell(top_row, 2, top_student)
        sheet.update_cell(top_row, 3, "")
        sheet.update_cell(top_row, 4, "")
        sheet.update_cell(top_row, 5, max_score)
        
        print(f"✅ 구글 시트에 결과가 추가되었습니다!")
        
    except Exception as e:
        print(f"❌ 구글 시트 업데이트 실패: {e}")
else:
    print(f"📋 시뮬레이션 모드 - 추가될 내용:")

print(f"\n📋 추가된 내용:")
print(f"   평균 행: ['평균', '', {korean_avg:.1f}, {english_avg:.1f}, {math_avg:.1f}]")
print(f"   최고점 행: ['최고점', '{top_student}', '', '', {max_score}]")

# 최종 결과 확인
if use_real_sheet:
    print(f"\n" + "="*50)
    print(f"📊 최종 성적표 (결과 포함):")
    print("="*50)
    
    try:
        final_values = sheet.get_all_values()
        for row in final_values:
            filtered_row = []
            for cell in row:
                if cell.strip():
                    filtered_row.append(cell)
            if filtered_row:
                print(filtered_row)
    except Exception as e:
        print(f"❌ 최종 결과 읽기 실패: {e}")
else:
    print(f"\n📋 시뮬레이션 최종 결과:")
    print("="*30)
    print("['번호', '이름', '국어', '영어', '수학']")
    print("['1', '홍길동', '80', '70', '60']")
    print("['2', '변사또', '90', '90', '80']")
    print("['3', '사임당', '70', '80', '100']")
    print("['평균', '', '80.0', '80.0', '80.0']")
    print("['최고점', '변사또', '', '', '260']") 