# ex4-3.py

# 딕셔너리 Dictionary( 사전 ) 한영사전 집(Key) -> House(Value)
# 키와 값의 쌍으로 이루어진 데이터를 저장하는 자료구조

# 빈 딕셔너리
empty_dict = {}
print( empty_dict )

person = {
    "name": "홍길동",
    "age": 30,
    "city": "한양"
}
print( person ) # {'name': '홍길동', 'age': 30, 'city': '한양'}

print( person['name'] )
print( person['age'] )
print( person['city'] )

print(person.get('name'))

