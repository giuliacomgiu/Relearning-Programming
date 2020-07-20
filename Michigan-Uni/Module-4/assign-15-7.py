# Reads data from iTunes in XML
# And creates a database with them

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Opening and parsing xml file
fname = input('Enter file name: ')
path = '/home/giuliacomgiu/Documents/Relearning-Programming/michigan-uni/tracks/'
if ( len(fname) < 1 ) : fname = path+'Library.xml'
stuff = ET.parse(fname)

# Defining function to find data. XML example:
# <key>Name</key><string>Another One Bites The Dust</string>
# i.key,i.text => key Name
# i.key,i.text => string Another One Bites ...
def lookup(d, key):
    content_next = False
    for child in d:

        # This runs 1 iter after
        # Correct header (content) and exits function.
        # No need to reset content_next 
        if content_next : return child.text
        
        #This runs only if correct header
        if child.tag == 'key' and child.text == key :
            content_next = True

    return None


# Reading XML
all_ = stuff.findall('dict/dict/dict')
print('Dict count:', len(all_))
for entry in all_:

    if ( lookup(entry, 'Track ID') is None ) : continue

    # If a Trck id was found, lookup contents
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    genre = lookup(entry, 'Genre')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    # If an information is missing, skip track
    if name is None or artist is None \
    or album is None or genre is None : 
        continue

    print(name, artist, album, count, rating, length)

    # Insert into database
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        ( name, album_id, genre_id, length, rating, count ) )

    conn.commit()
