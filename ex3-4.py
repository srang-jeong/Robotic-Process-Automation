# 연습문제
# 자판기 프로그램(무한루프)을 작성하시오.
cola = 3
cider = 2
orange = 4

while True:
    menu = input("콜라, 사이다, 오렌지, 종료: ")
    if menu == '종료':
        break
    if menu == '콜라':
        if cola > 0:
            cola -= 1
            print("콜라가 나옵니다")
        else:
            print("콜라 잔고가 떨어졌습니다.")
    elif menu == '사이다':
        if cider > 0:
            cider -= 1
            print("사이다가 나옵니다")
        else:
            print("사이다 잔고가 떨어졌습니다.")
    elif menu == '오렌지':
        if orange > 0:
            orange -= 1
            print("오렌지쥬스가 나옵니다")
        else:
            print("오렌지쥬스 잔고가 떨어졌습니다.")

# 텍스트 야구게임(무한루프)을 작성하시오.
import random

s = 0
b = 0
c = 0

while True:
    c += 1
    if random.randint(1, 100) <= 70:
        s += 1
        r = "스트라이크"
    else:
        b += 1
        r = "볼"
    if s == 3:
        print(f"{c}번 송구: {r} - {s}스트라이크 {b}볼 - 스트라이크 아웃!\n게임끝")
        break
    print(f"{c}번 송구: {r} - {s}스트라이크 {b}볼")
