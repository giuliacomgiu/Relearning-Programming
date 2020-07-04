#arithmetic operators
a=10.5
b=2

print('a: ',a)
print('b: ',b)
print('sum: ',a+b)
print('sub: ',a-b)
print('mult: ',a*b)
print('div: ',a/b)
print('div(floor): ',a//b)
print('module: ',a%b)
print('exponent: ',a**b)


#comparison operator
a=2
b=10

print('\n\ra: ',a)
print('b: ',b)
print('a > b is',a>b)
print('a < b is',a<b)
print('a == b is',a==b)
print('a != b is',a!=b)
print('a >= b is',a>=b)
print('a <= b is',a<=b)


#bitwise operator
a=5 #0101
b=3 #0011

print('\n\ra: ',a)
print('b: ',b)
print('a & b is',a&b)
print('a | b is',a|b)
print('~a',~a)
print('a xor b is',a^b)
print('a << 1 is',a<<1)
print('a >> b is',a>>b)
print('b << a is',b<<a)

#assignment operators
a=3

print('\n\ra: ',a)

a+=1
print('a+=1: ',a)

a-=1
print('a-=1: ',a)

a*=3
print('a*=2: ',a)

a/=3
print('a/=3: ',a)

a%=2
print('a%=2: ',a)

a**=2
print('a**=2: ',a)

a=7
print('a: ',a)
a&=3
print('a&=3: ',a)

a>>=1
print('a>>=1',a)

# identity operator
a=5.25
print('\n\ra: ',a)
print('float' if type(a) is float else \
	'int' if type(a) is int else \
	'Sorry, i don\'t know this type.')
a=7
print('\n\ra: ',a)
if type(a) is int:
	print('int')


#Membership operator
#Copy pasted shamelessly lol
str = 'Python operators'
dict = {6:'June',12:'Dec'}
print('\n\rstr: ', str)
print('dict: ', dict)
print('P in str: ',('P' in str)) 
print('ope in str: ',('ope' in str))
print('python not in str: ',('python' not in str))
print('6 in dict: ',(6 in dict)) 
print('Dec in dict: ',('Dec' in dict))