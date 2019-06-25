import sqlite3
connection = sqlite3.connect("dicebets.db")
cursor = connection.cursor()
cursor.execute("""DROP TABLE IF EXISTS dicebets""")
sql_command = """
CREATE TABLE dicebets ( 
id INT PRIMARY KEY,
dbuserId CHAR(32),
target INT, 
amount INT);"""
cursor.execute(sql_command)
connection.commit()
connection.close()

connection = sqlite3.connect("dicebets.db")
cursor = connection.cursor()
#sql_command = """INSERT INTO dicebets(dbuserId,target,amount) VALUES ({puser},{ptarget},{pamount});"""
#sql_command = sql_command.format(puser="132Beats",ptarget=1,pamount=100)
daten = ("132Beats",1,200)
cursor.execute("""INSERT INTO dicebets(dbuserId,target,amount) VALUES (?,?,?);""",daten)
connection.commit()
connection.close()

connection = sqlite3.connect("dicebets.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM dicebets") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("SELECT * FROM dicebets") 
print("\nfetch one:")
res = cursor.fetchone() 
print(res)