#Retrieving location using an
#outdated version of google maps api
#and json
import urllib.request, urllib.parse, urllib.error
import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Requesting location
addr_usr = ''
while len(addr_usr) < 1:
	addr_usr = input('Enter the location (case sensitive):')
	if len(addr_usr) > 1: break;
	print('It appears the input is too small') 

# Encoding string for web connection
addr = urllib.parse.urlencode({'key':42,\
	'address':addr_usr})

# website data
curl = 'http://py4e-data.dr-chuck.net/json?'
url = curl + addr
print("Retrieving",url)

# connecting and reading data
data = urllib.request.urlopen(url, context=ctx).read().decode()
print('Retrieved', len(data), 'characters')

# josn reading from string
try:
	data_js = json.loads(data)
except:
	data_js = None

# if nothing went wrong, print place id
if not data_js or 'status' not in data_js \
	or data_js['status'] != 'OK':
	print('=======FAILURE TO RETRIEVE========')
else:
	
	place_id = data_js['results'][0]['place_id']
	print('Place id',place_id) 
	#expected result ChIJbyeM79gpMYgRnELTRngZTwU