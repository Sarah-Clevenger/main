import sqlite3  
import json
import base64

con = sqlite3.connect('testy2.db')
cur = con.execute('SELECT * FROM entries ORDER BY idx')

db = {}
for row in cur:
    db[row[0]] = json.loads(row[1])
        
for i in db:
    db[i]['body'] = json.loads(base64.b64decode(db[i]['body']))