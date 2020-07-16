import urllib.request, urllib.parse, urllib.error
import ssl
import json


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Reading website
url_ = 'http://py4e-data.dr-chuck.net/comments_781443.json'
print("Enter location: ", url_)
print("Retrieving",url_)
data = urllib.request.urlopen(url_, context=ctx).read().decode()
print('Retrieved', len(data), 'characters')

#reading json
info = json.loads(data)
info_child = info['comments']
print('Count',len(info_child))

#sum of all counts
print(sum( [int(item['count']) for item in info_child ] ))