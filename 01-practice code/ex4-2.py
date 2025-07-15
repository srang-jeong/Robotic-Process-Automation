# 튜플 Tuple
# 리스트이면서 변경이 불가한 데이터 타입.
# 고정된 값을 전달할 때 사용한다. 함수의 반환값으로도 사용.

# 빈 튜플
empty_tuple = ()
print( empty_tuple )

# 튜플의 선언
numbers = (1, 2, 3, 4, 5)
print( numbers )
numbers2 = 10, 20, 30
print( numbers2 )
# 요소가 하나인 튜플은 쉼표 사용
numbers3 = (5) # 정수 5
numbers4 = (5,) # 튜플
print( numbers3 )
print( numbers4 )

# 함수의 반환값으로 튜플 사용
def get_user_data():
    return "김철수", 15, "서울"

name, age, city = get_user_data()
print( type(get_user_data()) )
print( name, age, city )