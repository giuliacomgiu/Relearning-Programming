from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl

#ignore ssl errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://py4e-data.dr-chuck.net/comments_781440.html'
html_ = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html_,"html.parser")

#find anchor tags
tags = soup('span')
print(sum( [int(tag.contents[0]) for tag in tags] ))
