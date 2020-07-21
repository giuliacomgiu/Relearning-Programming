# Creates database with Many to Many approach
# Storing Users, Courses and respective roles

import json
import sqlite3

# Creating database from scratch
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT UNIQUE
);

CREATE TABLE Course(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title TEXT UNIQUE
);

CREATE TABLE Member(
	role INTEGER NOT NULL,
	user_id INTEGER,
	course_id INTEGER,
	PRIMARY KEY(user_id,course_id)
);
	''')

# Reading data from json file
fname = input('Enter file name:')
if len(fname) < 1: fname = 'roster_data.json'
print('retreiving',fname)
data = open(fname).read()
jdata = json.loads(data)
print('retreived',len(jdata),'char')

# Inserting items to database
print('Inserting data to database\n...')
for item in jdata:
	name = item[0]
	title = item[1]
	role = item[2]

	if name == None or title == None\
		or role == None: continue

	cur.execute('''
		INSERT OR IGNORE INTO User(name) 
		VALUES (?)''', (name, ))
	cur.execute(''' SELECT id FROM User 
		WHERE name = ?''', (name, ))
	user_id = cur.fetchone()[0]

	cur.execute('''
		INSERT OR IGNORE INTO Course(title) 
		VALUES (?)''', (title, ))
	cur.execute(''' SELECT id FROM Course 
		WHERE title = ?''', (title, ))
	course_id = cur.fetchone()[0]

	cur.execute('''
		INSERT OR REPLACE INTO Member
		(role, user_id, course_id) VALUES (?, ?, ?)''',
		(role, user_id, course_id))
	conn.commit()

print('Success!')

# Necessary for coursera evaluation
cur.execute('''SELECT hex(User.name || Course.title || Member.role) AS X 
	FROM User JOIN Course JOIN Member 
	ON User.id = Member.user_id and
	Course.id = Member.course_id
	ORDER BY X''')
print(cur.fetchone()[0])
