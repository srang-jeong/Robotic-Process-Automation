import sqlite3

db_path = './13-dbms/students.db'

# 전체 학생 조회
conn = sqlite3.connect(db_path)
print( conn )

cursor = conn.cursor()

# 조건적인 검색 (WHERE절)
# query = 'SELECT * FROM student WHERE name = "홍길동"'
# cursor.execute( query )

query = 'SELECT * FROM student WHERE name = ? or name = ?'
cursor.execute( query, ('홍길동','이순신') ) # 튜플 타입으로 매개변수를 넣는다.

student_list = cursor.fetchall()

conn.close()

if student_list:
    for student in student_list:
        print( student )
        print(f"id:{student[0]}, name:{student[1]}, age:{student[2]}, grade:{student[3]}, create_at:{student[4]} ")
else:
    print("검색된 목록이 없습니다.")