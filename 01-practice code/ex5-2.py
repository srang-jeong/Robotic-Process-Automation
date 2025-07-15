# 종합 연습문제
# 숫자 맞추기 게임
문제설명 = '''
컴퓨터가 1부터 20 사이의 정수 중 하나를 무작위로 선택합니다.
사용자는 숫자를 추측하면서 컴퓨터가 선택한 숫자를 맞춰야 합니다.

<입출력 예시>
1~20 숫자 입력: 10
너무 작아요.
1~20 숫자 입력: 15
너무 커요.
1~20 숫자 입력: 13
정답입니다! 3번 만에 맞췄습니다.
'''
import random

def game():
    computer = random.randint(1, 20)
    count = 0

    while True:
        user = int(input(("1~20 숫자 입력: ")))
        count += 1

        if user < computer:
            print("너무 작아요.")
        elif user < computer:
            print("너무 커요.")
        else:
            print(f"정답입니다! {count}번 만에 맞췄습니다.")
            break
game()


