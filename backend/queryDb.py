import sqlite3

with sqlite3.connect('database.db') as connection:
    results = connection.execute('select * from drugs').fetchall()

for result in results:
    print(result, '\n')
