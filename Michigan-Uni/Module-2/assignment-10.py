#Opens file in their server
#https://www.py4e.com/code3/mbox-short.txt
#creates a histogram based on what hour
#the emails were received

name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)
hours = dict()

for line in handle:

#Find these lines
##From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
    if line.startswith("From "):
        words = line.split()
        time = words[5].split(':')
        hours[time[0]] = hours.get(time[0],0)+1


for key, val in sorted(hours.items()):
    print(key,val)
