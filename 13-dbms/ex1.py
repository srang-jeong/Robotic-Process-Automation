"""
SQLite 기초 CRUD 예제
- Create: 데이터 생성(추가)
- Read: 데이터 조회
- Update: 데이터 수정
- Delete: 데이터 삭제
"""
# sqlite3 라이브러리는 python에 기본설치 되어 있음.
import sqlite3

db_path = './13-dbms/students.db'

# 전체 학생 조회
conn = sqlite3.connect(db_path)
print( conn )

cursor = conn.cursor()
cursor.execute('SELECT * FROM students ORDER BY id')
student_list = cursor.fetchall()

conn.close()

print("\n===전체 학생 목록===")
if student_list:
    for student in student_list:
        print( student )
else:
    print("등록된 학생이 없습니다.")