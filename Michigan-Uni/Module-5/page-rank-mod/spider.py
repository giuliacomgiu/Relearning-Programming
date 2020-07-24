import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    url TEXT UNIQUE, 
    html TEXT,
    error INTEGER, 
    old_rank REAL, 
    new_rank REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links
    (from_id INTEGER, 
    to_id INTEGER, 
    UNIQUE(from_id, to_id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs 
    (url TEXT UNIQUE)''')

# Check to see if we are already in progress...
cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:
    print("Restarting existing crawl.  Remove spider.sqlite to start a fresh crawl.")
else :
    starturl = input('Enter permitted web url or enter: ')
    if ( len(starturl) < 1 ) : starturl = 'http://python-data.dr-chuck.net/'
    if ( starturl.endswith('/') ) : starturl = starturl[:-1]
    web = starturl
    if ( starturl.endswith('.htm') or starturl.endswith('.html') ) :
        pos = starturl.rfind('/')
        web = starturl[:pos]

    if ( len(web) > 1 ) :
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', ( web, ) )
        cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank) 
            VALUES ( ?, NULL, 1.0 )''', ( starturl, ) )
        conn.commit()

# Get the permitted websites to crawl
cur.execute('''SELECT url FROM Webs''')
webs = list()
for row in cur:
    webs.append(str(row[0]))

print(webs)

many = 0
print('System checking database for remaining pages to crawl')

# Crawl
while True:

    # Prompt user for number of crawls
    if ( many < 1 ) :
        sval = input('How many pages:')
        if ( len(sval) < 1 ) : break
        many = int(sval)
    many = many - 1

    # Selecting a page not yet crawled (html and error empty)
    cur.execute('SELECT id,url FROM Pages WHERE html is NULL\
        and error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        fromid, url = cur.fetchone()
        #fromid = row[0]
        #url = row[1]
    except:
        print('No unretrieved HTML pages found')
        break

    print(fromid, url, end=' ')

    # Making sure the new url is not in Links table
    cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) )
    
    # Reading url
    try:
        document = urlopen(url, context=ctx)

        html = document.read()
        
        # Error if status not 200
        if document.getcode() != 200 :
            print("Error on page: ",document.getcode())
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) )
            conn.commit()
            continue

        # Error if content type not text/html
        if 'text/html' != document.info().get_content_type() :
            print("Ignore non text/html page")
            cur.execute('UPDATE Pages SET error=? WHERE url=?', (-2, url) )
            conn.commit()
            continue

        print('('+str(len(html))+')', end=' ')

        soup = BeautifulSoup(html, "html.parser")
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except:
        print("Unable to retrieve or parse page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
        conn.commit()
        continue

    # Inserting new page on db
    cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( url, ) )
    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url ) )
    conn.commit()

    # Collecting its links
    # Retrieve all of the anchor tags
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href', None)
        if ( href is None ) : continue
        
        # Resolve relative references like href="/contact"
        up = urlparse(href)
        if ( len(up.scheme) < 1 ) :
            href = urljoin(url, href)
        ipos = href.find('#')
        if ( ipos > 1 ) : href = href[:ipos]
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue
        if ( href.endswith('/') ) : href = href[:-1]
        # print href
        if ( len(href) < 1 ) : continue

		# Check if the URL is a permitted link
        found = False
        for web in webs:
            if ( href.startswith(web) ) :
                found = True
                break
        if not found : continue

        # Trying to add to database
        try:
            cur.execute('SELECT id FROM Pages ORDER BY id DESC')
            newid = cur.fetchone()[0] + 1
        except: 
            newid = None
            print('Couldn\'t check id')
            continue

        try:
            toid = newid
            cur.execute('INSERT OR IGNORE INTO Pages (id, url, html, new_rank) VALUES ( ?, ?, NULL, 1.0 )', ( newid, href, ) )
            cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) )
            conn.commit()
            count = count + 1
        except:
            print('Couldn\'t add to table')
            continue
    
    print(count)

cur.close()
