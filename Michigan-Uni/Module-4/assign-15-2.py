# Counts emails received and stores in db
import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Reading file from web
#url_ = 'https://py4e.com/code3/mbox.txt'
#print("Retrieving",url_)
#data = urllib.request.urlopen(url_, context=ctx).read().decode()
#print('Retrieved', len(data), 'characters')
with open('mbox.txt') as file:
    data = file.readlines()
    print('Retrieved', len(data), 'characters')

# Connecting to SQLite DB
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()
print('Connected to db')

# Setting up the db
cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# Reading and storing data
for line in data:
    
    if not line.startswith('From: '): continue 

    # Processing received messages
    pieces = line.split()
    email = pieces[1].split('@')
    org = email[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

# Finding most received orgs
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()