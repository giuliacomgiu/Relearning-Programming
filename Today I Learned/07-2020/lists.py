##INITIALIZATION
#initializing a list matrix
print('INITIALIZATION')
sq_matrix = [[0,1,2],[3,4,5],[6,7,8]]
print('manual initialization ', sq_matrix)


#initialization w loops
sq_matrix = []
for row in range(3):
	matrix_row =[]
	for col in range(3):
		matrix_row.append(3*row+col) 
	sq_matrix.append(matrix_row)

print('looped initialization: ',sq_matrix)


#condensing initialization
print('\n\rCONDENSATION')
sq_matrix = []
for row in range(3):
	sq_matrix.append([3*row+col for col in range(3)])
print('one condesnation initialization: ',sq_matrix)


#condensing even further
sq_matrix = [[3*row+col for col in range(3)] for row in range(3)]
print('two condesnations initialization: ', sq_matrix)

##TRANSPOSING
print('\n\rTRANSPOSITION')
sq_matrix=[[row[col] for row in sq_matrix] for col in range(len(sq_matrix))]
print('transpose:',sq_matrix)

##built in transposition
sq_matrix = (list(zip(*sq_matrix)))
print('built in transposition: ',sq_matrix)

print('\n\rREPLICATION')
##REPLICATION INITIALIZATION
sq_matrix = [[0,1,2]]*3
print('replication initialization: ',sq_matrix)

sq_matrix[0].append(3)
print('replication mod: ',sq_matrix)
print('BE CAREFUL! Replication doesnt actually make a copy of a list:')
print('matrix[0] memory loc: ', id(sq_matrix[0]))
print('matrix[1] memory loc: ', id(sq_matrix[1]))

print("""\n\tThere are other uses for lists, such as stacks!
\tThey're good LIFOs, but bad FIFOs, because the processor has 
\tto shift all items of the list in order to get to the first one.\n\r""")