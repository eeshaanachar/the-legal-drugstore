import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute('create table if not exists drugs (id integer primary key autoincrement, name text, short_desc text, long_desc text, link text)')

with open('to_insert.txt') as fh:
    content = fh.read().splitlines()

for i in range(0, len(content), 5):
    cursor.execute('insert into drugs (name, short_desc, long_desc, link) values (?, ?, ?, ?)', content[i : i+4])

connection.commit()
connection.close()
