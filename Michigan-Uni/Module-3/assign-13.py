#finds text elements "count",
#great grand children of root
#and sums them

import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Reading website
url_ = 'http://py4e-data.dr-chuck.net/comments_781442.xml'
print("Enter location: ", url_)
print("Retrieving",url_)
data = urllib.request.urlopen(url_, context=ctx).read().decode()
print('Retrieved', len(data), 'characters')

# XML processing and sum
tree = ET.fromstring(data)
counts = tree.findall('./comments/comment/count')
print("Count",len(counts))
print(sum( [int(value.text) for value in counts] ))