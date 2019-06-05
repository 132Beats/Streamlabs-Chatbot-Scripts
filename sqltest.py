
sql_command = """
CREATE TABLE dicebets (, , );"""

import sqlite3
connection = sqlite3.connect("dicebets.db")

cursor = connection.cursor()

cursor.execute("""DROP TABLE dicebets;""")

sql_command = """
CREATE TABLE dicebets ( 
userId CHAR(8) PRIMARY KEY, 
target INT, 
amount INT);"""

cursor.execute(sql_command)

#sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
#cursor.execute(sql_command)


#sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
#cursor.execute(sql_command)

# never forget this, if you want the changes to be saved:
connection.commit()

connection.close()