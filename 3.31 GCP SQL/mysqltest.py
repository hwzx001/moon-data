import pymysql 
import pymysql.cursors

# Connect to the database
connection=pymysql.connect(
        host="35.224.151.74", #ip
        user="root",# usr name
        password="******", #pwd
        db="test", # db name
        charset='utf8'
    )

try:
    with connection.cursor() as cursor:
         sql = "SELECT * FROM `users` "
         cursor.execute(sql)
         result=cursor.fetchone()
         print(result)
finally:
    connection.close()

