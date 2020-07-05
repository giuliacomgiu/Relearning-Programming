#INIT
location = ()
print('location: ',location)

location = 3.214,
print('location: ',location)

location = 3.214,1.005
print('location: ',location)

location = ([2*y for y in range(2)],[1+2*y for y in range(2)])
print('location: ',location)

ana, julio = location
print('unpacking: ANA-',ana,' JULIO-',julio)

location = ((3.214,1.005),)*3
print('replication: ',location)

print("""\tReplication in tuples works a little differently than Lists.
	See, because in order to initialize 1 item tuples the syntax is
	'tuple = element', . For the replication of tuples within tuples, the 
	program should be: tuple = ((thing1,thing2),)*n.
	If the comma is absent, python will only replicate the elements.""")

del location
