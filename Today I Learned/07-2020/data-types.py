# Strings
str = 'String encapsulated in one quotation mark'
print(str)

str = "String encapsulated in double quotation marks"
print(str)

str = """Multi line string.
Three quotation marks.
The strings in Python are immutable. 
The memory will be allocated once 
and re-used thereafter."""
print(str)

#Lists
list_1 = [1,1+1j,'list_1',b'255']

print('\n\rLISTS')
for item in list_1:
	print('Item is ',item,' and its type is',type(item))

#Nested list, or, as I like to call it,
	#this is not a matrix. Fuck up potential.
list_1 = [1,1+1j,'list',[2,3,4]]
print('\n\r')
for item in list_1:
	print(item)
print('Item nr 0 is ',list_1[0])
print('Item nr 3,0 is',list_1[3][0])

#Slicing lists
list_1 = ['C', 'C++', 'Python', 'Java', 'Go', 'Angular']
print('list[0:3]',list_1[0:3])

#Now, tuples / nested tuples
#some cpy pasting was involved.
print('\n\rTUPLES')
tuple_obj = 0
first_tuple = (tuple_obj, 5, 7, 9)
second_tuple = ('learn', 'python 3')
nested_tuple = (first_tuple, second_tuple)
print(nested_tuple)
tuple_obj = 1
print(first_tuple)
