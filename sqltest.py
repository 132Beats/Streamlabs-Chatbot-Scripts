import sqlite3
connection = sqlite3.connect("dicebets.db")

cursor = connection.cursor()
cursor.execute("""DROP TABLE IF EXISTS dicebets""")
sql_command = """
CREATE TABLE dicebets ( 
userId CHAR(8) PRIMARY KEY, 
target INT, 
amount INT);"""

cursor.execute(sql_command)

sql_command = """INSERT INTO dicebets (userId, target, amount)
    VALUES ("__dicebot__", 1, 100);"""
cursor.execute(sql_command)

connection.commit()

connection.close()