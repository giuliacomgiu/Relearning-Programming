import sqlite3
import ssl
import urllib.robotparser
from urllib.request import urlopen
from urllib.parse import urlparse,urlunparse
from bs4 import BeautifulSoup

# Prompt url - NOT NECESSARY
'''url = input('Enter url or enter:')
if len(url) < 1: url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
url_p = urlparse(url)
if url_p.scheme == None or url_p.netloc == None:
	print('There was something wrong with the url',url)
	quit()
print('Default:',url)'''

def find_links():
	print('GETTING LAST STATEMENTS\' URLS FROM')

	# Checking robots.txt file
	url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
	print(url)
	url_p = urlparse(url)
	robot_p = url_p._replace(path='/robots.txt',params='',query='',fragment='')
	robot_u = urlunparse(robot_p)
	print('Attempting to open robots.txt as', robot_u)
	try:
		robot = urllib.robotparser.RobotFileParser()
		robot.set_url(robot_u)
		robot.read()
		auth = robot.can_fetch('*',url)
		print('Authorization for crawling is',auth)
		if auth != True: input('Proceed at your own risk')
	except:
		input('Couldnt open robots.txt, proceed at your own risk:')


	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	#Opening url
	try:
		with urlopen(url,context=ctx) as doc:
			if doc.getcode() != 200:
				print('Error on page: ',url,'\n',doc.getcode())
				raise ValueError('Couldnt open page')

			if 'html' not in doc.info().get_content_type():
				raise ValueError('Non html page')
			u_raw = doc.read()
	except ValueError as err:
		print(err)
		quit()
	except:
		print('Couldnt open for reasons unknown')

	# Parsing
	u_soup = BeautifulSoup(u_raw, 'html.parser')

	file = input('Would you like to save to a file? (y/n):')
	if file.lower() == 'y':
		fname = input('Enter file name')
		with open(fname,'w') as f:
			print(u_soup.prettify(),file=f)

	# Paths for last statement and offender info
	u_lwords = []
	u_info = []
	for link in u_soup.find_all('a'):
		if "Last Statement of" in str(link):
			u_lwords.append(link)
		if "Offender Information for" in str(link):
			u_info.append(link)

	# Replacing old list with actual urls
	for link in u_lwords: 
		path = '/death_row/'+link['href']
		i = u_lwords.index(link)
		new_parse = url_p._replace(path=path,params='',query='',fragment='')
		u_lwords[i] = urlunparse(new_parse)

	for link in u_info: 
		path = '/death_row/'+link['href']
		i = u_info.index(link)
		new_parse = url_p._replace(path=path,params='',query='',fragment='')
		u_info[i] = urlunparse(new_parse)

	return u_lwords,u_info

def crawler(lwords,info):
	db = input('Enter new db name or enter for default:')
	'''if len(db) < 1: db = 'last-words'
	conn = sqlite3.connect(db+'.sqlite')
	cur = conn.cursor()
'''
	"""cur.execute('''CREATE TABLE IF NOT EXISTS Inmate(
		name TEXT,
		age INTEGER,
		last_words TEXT,
		education_id INTEGER,
		race_id INTEGER, 
		gender_id INTEGER)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Education(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		education INTEGER UNIQUE)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Race(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		race TEXT UNIQUE)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Gender(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		gender TEXT UNIQUE)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Words(
		count INTEGER,
		word TEXT UNIQUE)''')"""

	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	# Opening link
	# Loop runs till end even if number of links is diff
	for i in range(max(len(lwords),len(info))):
		try:
			with urlopen(lwords[i],context=ctx) as doc:
				if doc.getcode() != 200:
					print('Error on page: ',lwords[i],'\n',doc.getcode())
					raise ValueError('Couldnt open page')

				if 'html' not in doc.info().get_content_type():
					raise ValueError('Non html page')
				u_raw = doc.read()
		except ValueError as err:
			print(err)
			continue
		except:
			print('Couldnt open for reasons unknown')
			quit()

		print('yay')
		soup = BeautifulSoup(u_raw,'html.parser')
		print(soup.find("Last Statement"))
		input('pause')		



lwords,info = find_links()
crawler(lwords,info)