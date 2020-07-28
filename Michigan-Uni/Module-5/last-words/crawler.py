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

def openReadHTML(url):
	success = False
	raw = None

	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	#Open Html
	try:
		with urlopen(url,context=ctx) as doc:
			if doc.getcode() != 200:
				print('Error on page: ',url,'\n',doc.getcode())
				raise ValueError('Couldnt open page')

			if 'text/html' not in doc.info().get_content_type():
				raise ValueError('Non html page')
 			
 			# Read page
			success = True
			raw = doc.read()
	except ValueError as err:
		print(err)
	except KeyboardInterrupt:
		quit()
	except:
		print('Couldnt open for reasons unknown')

	return success, raw

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
	success, u_raw = openReadHTML(url)
	if success != True: 
		print('Couldnt get offernder\'s urls')
		quit()

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
		if u_lwords[i] == 'https://www.tdcj.texas.gov/death_row/dr_info/no_last_statement.html':
			u_lwords[i] = ''
	s = input('Would you like to save last words urls in a file? (y/n)')
	if(s.lower() == 'y'): saveFile(u_lwords,'url_last_words')

	for link in u_info: 
		path = '/death_row/'+link['href']
		i = u_info.index(link)
		new_parse = url_p._replace(path=path,params='',query='',fragment='')
		u_info[i] = urlunparse(new_parse)
		if u_info[i] == 'https://www.tdcj.texas.gov/death_row/dr_info/no_info_available.html':
			u_info[i] = ''
	s = input('Would you like to save info urls in a file? (y/n)')
	if(s.lower() == 'y'): saveFile(u_info,'url_info')

	return u_lwords,u_info

def nameParser(name):
	name = str(name)
	name = name.strip(' </p>').split('#')[0].strip()
	name = name.rstrip(' 	,TDCJ-')
	
	#Correcting 'Garza, Jr., Manuel'
	if ',' in name:
		full_name = name.split(',')
		if len(full_name) > 2: print('Check',name)
		name = full_name.pop(-1).strip(' 	.')
		for word in full_name:
			name += ' ' + word.strip(' 	.')
	return name

def infoFinder(info,html_ref):
	while info not in html_ref:
		html_ref = html_ref.next_element
	result = str(html_ref.next_element.next_element.next_element.string)

	# Fixing last words bug but maintaining age/edu integrity
	if result.isdecimal() == False and len(result) <= 1:
		result = str(html_ref.next_element.next_element.next_element.next_element.string)
	return result

def wordCounter(sentence):
	word_count = dict()
	words = sentence.lower().strip('\'"').split()

	for word in words:
		word = word.strip(' \t.,"!?-')

		if word.isalpha() or word.isdecimal():
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1

		# Considering words with apostrophes (let's)
		elif "'" in word:
			parts = word.split("'")
			for part in parts: 
				if part.isalpha():
					if word in word_count:
						word_count[word] += 1
					else:
						word_count[word] = 1

	return word_count

def createDatabase():
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
		word TEXT UNIQUE,
		count INTEGER)''')

	conn.close()
	return db+'.sqlite'

def getData(url_lwords,url_info,db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	
	# Opening and reading offender info
	success, raw = openReadHTML(url_info)
	if success != True: 
		name = ''
	else:
		# Parsing
		soup = BeautifulSoup(raw,'html.parser')
		main = soup.find(id='maincontent')

		name = infoFinder('Name',main)
		name = nameParser(name)
		age = infoFinder('Age (',main)
		edu = infoFinder('Education',main)
		edu = edu.lower().strip(' abcdefghijklmnopqrstuvwxyv.()')
		race = infoFinder('Race',main).lower()
		gender = infoFinder('Gender',main).lower()
		print(name,age,race,gender)

		# Inserting on db
		if edu != None:
			cur.execute('''INSERT OR IGNORE INTO 
				Education(education) VALUES (?)''',(edu,))
			cur.execute('''SELECT id FROM Education 
				WHERE education = ?''',(edu,))
			edu_id = cur.fetchone()[0]

		if race != None:
			cur.execute('''INSERT OR IGNORE INTO 
				Race(race) VALUES (?)''',(race,))
			cur.execute('SELECT id FROM Race WHERE race = ?',(race,))
			race_id = cur.fetchone()[0]

		if gender != None:
			cur.execute('''INSERT OR IGNORE INTO 
			Gender(gender) VALUES (?)''',(gender,))
			cur.execute('SELECT id FROM Gender WHERE gender = ?',(gender,))
			gender_id = cur.fetchone()[0]

		if name != None:
			cur.execute('''INSERT OR IGNORE INTO 
			Inmate(name,age,education_id,race_id,gender_id) 
			VALUES (?, ?, ?, ?, ?)''',(name, age, edu_id, race_id, gender_id))
			conn.commit()

	# Aquire correspondent name from Offender info 
	name_i = name

	# Attempts to open Last words' url
	success, raw = openReadHTML(url_lwords)
	if success != True: last_words = ''
	else:
		# Parsing
		soup = BeautifulSoup(raw,'html.parser')
		f = soup.find(id='maincontent')
		
		# Finding name
		elem = infoFinder('Offender:',f)
		name = nameParser(elem)

		# Checking name compatibility.
		# The names from last words often
		# Dont include middle names.
		count = 0
		for word in name.split():
			if word in name_i: count +=1
			if count > 1: 
				name = name_i
				break

		# Finding last statement
		last_words = infoFinder('Last Statement:',f)
		last_words = last_words.strip('  	</p>').strip()
		
		#print(last_words,end='\n\n')

    	# Inserting on database
		if name != None and last_words != None:
			cur.execute('''INSERT OR IGNORE INTO Inmate(name, last_words)
				VALUES (?, ?)''',(name, last_words))
			cur.execute('''UPDATE Inmate SET last_words=? WHERE name=?''',
				(last_words,name))
			conn.commit()

	conn.close()
	return last_words


word_count = dict()

# Get all offender urls from texas website
u_lwords,u_info = findLinks()
lwords_small = u_lwords[455:]
info_small = u_info[455:]

# Making sure both lists are the same size
diff = len(u_lwords) - len(u_info)
if diff > 0:
	for i in range(diff): u_info.append('')
elif diff < 0:
	for i in range(diff): u_lwords.append('')

db_name = createDatabase()

# Replace lwords_small w u_lwords
# Get offender's data and last words,
# store in database, count words
for i in range(len(lwords_small)):
	
	last_words = getData(lwords_small[i],info_small[i],db_name)
	sentence_count = wordCounter(last_words)
	
	if len(sentence_count) > 3:
		for k,v in sentence_count.items():
			if k in word_count: word_count[k] += v
			else: word_count[k] = v

print(word_count)
conn = sqlite3.connect(db_name)
cur = conn.cursor()
for word, count in word_count.items():
	cur.execute('''INSERT OR IGNORE INTO Words(word,count)
		VALUES (?, ?)''', (word, count))
	cur.execute('''UPDATE Words SET count=? 
		WHERE word=?''', (count, word))
	conn.commit()
conn.close()
