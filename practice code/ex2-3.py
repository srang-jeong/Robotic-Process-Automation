#1. 문자열 출력하기
a = "Python is easy!"
print(a)
# 2. 문자열 인덱싱
s = "Hello Python"
print(s[0])
print(s[-1])
# 3. 문자열 슬라이싱
s = "Life is short, use Python"
print(s[-10:])
# 4. 문자열 합치기
a = "Python"
b = " is fun"
print(a+b)
# 5. 문자열 곱하기
print("Hi! "*3)
# 6. 문자열 포매팅
print( "I ate %d apples " % 5  )
# 7. 문자열 함수 - count()
a = "banana"
print( a.count('a'))
# 8. 문자열 함수 - find()와 index() 차이
a = "hello"
print( a.find('e'))
print( a.index('e'))
print( a.find('z'))
# print( a.index('z')) 인덱스 오류
# 9. 문자열 나누기
a = "apple,banana,grape"
print(a.split(','))
# 10. 문자열 바꾸기
a = "I love Java"
print(a.replace('Java', "Python"))