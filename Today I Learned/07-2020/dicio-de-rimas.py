path_dir = "/home/giuliacomgiu/Documents/dicio-de-rimas/"
path_orig_file = "port-wlp.txt"
path_short_file = "port-wlp-shrunk.txt"

lines = []

#reading first n lines
with open(path_dir+path_orig_file) as port_wlp:
	lines.extend(port_wlp.readline() for i in range(1000))

#removing problematic line
lines.pop(0)


with open(path_dir+path_short_file,'w') as short_port:
	for line in lines:
		splt_line = line.split('\t')
		short_port.write(splt_line[2] + ',' + splt_line[4])
