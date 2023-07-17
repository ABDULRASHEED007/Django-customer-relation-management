

import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="W@2915djkq#",
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE Mysqlbases")

print("All Done!")