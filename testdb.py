#check to see if we can connect to MySQL
import pymysql

#change the databse information to reflect your own
#open database connection
db = pymysql.connect('servername','username','password','tablename')

#prepare a cursor object
cursor = db.cursor()

#execute SQL Query
cursor.execute("SELECT VERSION()")

#fetch row
data = cursor.fetchone()

print("Database version: %s" % data)

#disconnect from server
db.close()
