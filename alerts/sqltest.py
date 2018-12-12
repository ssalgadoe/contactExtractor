import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',user='capstone_user',password='dupa',
                             db='capstone',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `feeds` (`title`, `link`,`description`,`keywords`) VALUES (%s, %s,%s,%s)"
        cursor.execute(sql,('title2', "www.cnn.com/feeds3",'this is description2','kw1,kw2,kw2'))
        connection.commit()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `feeds`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
