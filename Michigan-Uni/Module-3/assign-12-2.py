#follows a series of links and prints out the names
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import re

#ignore ssl errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#initialization
url = 'http://py4e-data.dr-chuck.net/known_by_Sheridan.html'
link_pos = 17 #starting counting w 0
num_follow = 7

for i in range(num_follow):
	#open current link
	html_ = urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html_,"html.parser")

	#finds the next link
	tags = soup('a')
	url = tags[link_pos].get('href',None)
	name = re.findall('by_(.+)\.html',url)
	print(name)
	i += 1
