##FINDS ALL NUMBERS IN FILE
##AND SUMS THEM

import re

file = "regex_sum_781438.txt"

with open(file) as full_text:
	numbers = re.findall('[0-9]+',full_text.read())

sum_ = 0
for item in numbers:
	sum_ += int(item)

print(sum_)

##LIST COMPREHENSION
print(sum( [int(n) for n in re.findall('[0-9]+',open(file).read())] ))