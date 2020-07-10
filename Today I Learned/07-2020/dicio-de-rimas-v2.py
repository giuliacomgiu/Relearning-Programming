#defining directories
path_dir = "/home/giuliacomgiu/Documents/dicio-de-rimas/"
file_orig = "port-wlp.txt"
file_new = "port-wlp-shrunk.txt"

def openFile(file_name, path_dir, n_lines=4, lines=None):
	lines = []

#reading first n lines
	with open(path_dir+file_name) as open_file:
		lines.extend(open_file.readline().strip('\x00')\
			for i in range(n_lines))
		return lines

def processFile(lines,lines_proc=None):
	lines_proc = []

	#removing problematic header
	lines.pop(0)

	#split items, if it's a word
	#append to lines_proc and return it
	for line in lines:
		
		#doc is in a weird as hell encoding
		#that adds '\x00' in front of every char
		#tried to encode decode in several ways
		#this was the only thing that worked:
		splt_line = line.replace('\x00','').split('\t')

		#tries to find word on traditional method
		if splt_line[2].isalpha() == True:
			lines_proc.extend(splt_line[2].lower()\
				+ ',' + splt_line[4])

	return lines_proc

def writeFile(lines,file_name,path_dir):
	with open(path_dir+file_name,'w') as open_file:
		for line in lines:
			open_file.write(line)


lines = openFile(file_orig, path_dir,1000)
new_lines = processFile(lines)
writeFile(new_lines,file_new,path_dir)
		
