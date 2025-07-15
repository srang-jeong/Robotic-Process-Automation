# 리스트 

# 빈 리스트
empty_list = []
print( empty_list )

numbers = [1, 2, 3, 4, 5]
mixed_list = [ "apple", 123, 3.14, True ]
nested_list = [ [1,2], ["a", "b"], [True, False] ]

print( numbers[0] )
print(numbers[:3])
print(numbers[1:])

q = []
	
q.append(4)
q.extend([6, 7, 8])
q.insert(1, 5)
q.remove(7)
q.index(8)
q.pop()
print(q)

w = [2, 0, 4, 3, 1]
w.sort()
print(w)

w.reverse()
print(w)