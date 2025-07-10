# 조건문
# 특정 조건이 참일 때만, 코드를 실행하게 단다. 선택적 실행.
# if 조건:
#    조건이 참일 때 실행될 코드(들여스기 필수!)

# 단순 if문
score = 55
if score >= 60:
    print("합격입니다!") 

# if else문
age = 15
if age>= 18:
    print("성인입니다!") 
else:
    print("미성년자입니다!")

# if elif문
month = 6
if month <= 3:
    print("1,2,3월")
elif month <= 6:
    print("4,5,6월")

# if elif else문
month = 6
if month <= 3:
    print("1,2,3월")
elif month <= 6:
    print("4,5,6월")
else:
    print("그 외의 월")

# 연습문제
# 1. 마이클의 영어 점수를 입력받고,
# 영어 점수가 90점 이상이면, 'A학점'
# 영어 점수가 80점 이상이면, 'B학점'
# 영어 점수가 70점 이상이면, 'C학점'
# 영어 점수가 60점 미만이면, 'D학점' 으로 출력하시오.
Michael = int(input("마이클의 영어점수?: "))
if Michael >= 90:
    print("A학점")
elif Michael >= 80:
    print("B학점")
elif Michael >= 70:
    print("C학점")
else:
    print("D학점")

#2. 오늘의 날씨 예보 출력
# 랜덤값으로 0, 1, 2 중 하나의 수를 발생시키고
# 0이면, "오늘의 날씨는 비 입니다. 우산을 챙기세요!"
# 1이면, "오늘의 날씨는 흐림 입니다. 나들이 가기 좋을 수도 있어요."
# 2이면, "오늘의 날씨는 맑음 입니다. 화창한 하루 되세요!"
# 을 출력하시오.
import random
random_int = random.randint(0,2)
print(random_int)

if random_int == 0:
    print("오늘의 날씨는 비 입니다. 우산을 챙기세요!")
elif random_int == 1:
    print("오늘의 날씨는 흐림 입니다. 나들이 가기 좋을 수도 있어요.")
else:
    print("오늘의 날씨는 맑음 입니다. 화창한 하루 되세요!")

