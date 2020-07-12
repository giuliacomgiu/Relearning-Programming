##FINDS ALL NUMBERS IN FILE
##AND SUMS THEM

import re

file = "regex_sum_42.txt"

with open(file) as full_text:
	numbers = re.findall('[0-9]+',full_text.read())

sum = 0
for item in numbers:
	sum += int(item)

print(sum)
