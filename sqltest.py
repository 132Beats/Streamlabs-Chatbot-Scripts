
sql_command = """
CREATE TABLE dicebets (, , );"""

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


#sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
#cursor.execute(sql_command)

# never forget this, if you want the changes to be saved:
connection.commit()

connection.close()