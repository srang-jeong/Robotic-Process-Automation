# 반복문: 반복적으로 코드르르 수행하는 문장
# for 변수 in 리스트(또는 튜플, 문자열):
# while 조건문:
# 0~4까지 5번 반복

# for i in range(5):
    # print(f'반복 횟수: {i}')

# for i in range(1,20):
    # print(f'반복 횟수: {i}')

# num = 0
# while num <5:
    # num = num + 1
    # print(f'반복횟수: {num}')

# 연습문제
for i in range(1, 101):
    if i % 2 == 0:
        print('2의 배수:', i)

for i in range(1, 101):
    if i % 2 == 0 and i % 3 == 0:
        print('2의 배수 이면서 3의 배수:', i)

sum = 0 
for i in range(1, 101):
    sum = sum + i
print('1부터 100까지 합:', sum)

for i in range(1, 101):
    if '3' in str(i):
        print('3이 들어간 수:', i)