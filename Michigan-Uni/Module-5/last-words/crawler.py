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

def saveFile(content,fname=''):
	success = False
	f = input('Enter a valid file name or enter for default:')
	if len(f) > 1: fname = f
	print('Saving to file',fname)
	
	try:
		content = str(content)
		success = True
	except:
		print(type(content), 'cant be converted to string. Cant save')

	if success == True:	
		try:
			with open(fname,'w') as f:
				print(content,file=f)
		except:
			print('Couldn\'t open or write file.')
			success = False
	return

def findLinks():
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

	f = input('Would you like to save to a file? (y/n)')
	if f.lower == 'y': saveFile(u_soup.prettify(),'raw_html')

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
	s = input('Would you like to save last words urls in a file? (y/n)')
	if(s.lower() == 'y'): saveFile(u_lwords,'url_last_words')

	for link in u_info: 
		path = '/death_row/'+link['href']
		i = u_info.index(link)
		new_parse = url_p._replace(path=path,params='',query='',fragment='')
		u_info[i] = urlunparse(new_parse)
	s = input('Would you like to save info urls in a file? (y/n)')
	if(s.lower() == 'y'): saveFile(u_info,'url_info')

	return u_lwords,u_info

def nameParser(name):
	name = str(name)
	name = name.strip(' </p>').split('#')[0].strip()
	name = name.rstrip(' 	,TDCJ-')
	
	#Correcting 'Garza, Jr, Manuel'
	if ',' in name:
		full_name = name.split(',')
		if len(full_name) > 2: print('Check',name)
		name = full_name.pop(-1).strip()+' '
		for word in full_name:
			name += word.strip() + ' '
		name = name.strip()
	return name

def infoFinder(info,html_ref):
	while info not in html_ref:
		html_ref = html_ref.next_element
	result = str(html_ref.next_element.next_element.next_element.string)
	return result

def crawler(lwords,info):
	db = input('Enter new db name or enter for default:')
	if len(db) < 1: db = 'last-words'
	conn = sqlite3.connect(db+'.sqlite')
	cur = conn.cursor()

	cur.execute('''CREATE TABLE IF NOT EXISTS Inmate(
		name TEXT UNIQUE,
		age INTEGER,
		last_words TEXT,
		education_id INTEGER,
		race_id INTEGER, 
		gender_id INTEGER
		error INTEGER)''')

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
		word TEXT UNIQUE)''')

	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	# Opening and reading last words url link
	all_lwords = []
	for url in info:
		try:
			with urlopen(url,context=ctx) as doc:
				if doc.getcode() != 200:
					print('Error on page: ',url,'\n',doc.getcode())
					raise ValueError('Couldnt open page')

				if 'text/html' not in doc.info().get_content_type():
					raise ValueError('Non html page')

				raw = doc.read()
		except ValueError as err:
			print(err)
			continue
		except KeyboardInterrupt:
			break
		except:
			print('Couldnt open for reasons unknown')

		# Parsing
		soup = BeautifulSoup(raw,'html.parser')
		main = soup.find(id='maincontent')

		name = infoFinder('Name',main)
		name = nameParser(name)
		age = infoFinder('Age (',main)
		race = infoFinder('Race',main)
		gender = infoFinder('Gender',main)
		print(name,age,race,gender)

	for url in lwords:
		try:
			with urlopen(url,context=ctx) as doc:
				if doc.getcode() != 200:
					print('Error on page: ',url,'\n',doc.getcode())
					raise ValueError('Couldnt open page')

				if 'text/html' not in doc.info().get_content_type():
					raise ValueError('Non html page')

				raw = doc.read()
		except ValueError as err:
			print(err)
			continue
		except KeyboardInterrupt:
			break
		except:
			print('Couldnt open for reasons unknown')
			continue

		# Parsing
		soup = BeautifulSoup(raw,'html.parser')
		f = soup.find(id='maincontent')
		while 'Offender:' not in f:
			f = f.next_element
		
		# Finding name
		elem = str(f.next_element.next_element.next_element)
		name = nameParser(elem)
		print(name)

		# Finding last statement
		while 'Last Statement:' not in f:
			f = f.next_element
		last_words = str(f.next_element.next_element.next_element)
		last_words = last_words.strip('  	</p>')
		all_lwords.append(last_words)
		print(last_words)

		cur.execute('''INSERT INTO Inmate(name, last_words)
			VALUES (?, ?)''',(name,last_words))
		conn.commit()
	conn.close()



lwords,info = findLinks()
crawler(lwords,info)