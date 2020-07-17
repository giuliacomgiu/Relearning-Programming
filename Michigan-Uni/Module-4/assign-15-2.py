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
CREATE TABLE Counts (email TEXT, count INTEGER)''')

# Reading and storing data
for line in data:
    
    if not line.startswith('From: '): continue 

    # Processing received messages
    pieces = line.split()
    email = pieces[1]
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, 1)''', (email,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    (email,))
    conn.commit()

# Finding most received emails
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'
count_ = []
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])
    count_.append(row[1])

print(sum(count_))
cur.close()