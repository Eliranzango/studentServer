import sqlite3
from sqlite3 import OperationalError
conn = sqlite3.connect('app/mydatabase.db')
c = conn.cursor()

f = open(r"C:\Users\elira\Desktop\python\flask-sqlite-master\flask-sqlite-master\schema.sql")
full_sql = f.read()
sql_commands = full_sql.replace('\n', '').split(';')[:-1]
for sql_command in sql_commands:
  c.execute(sql_command)

c.close()