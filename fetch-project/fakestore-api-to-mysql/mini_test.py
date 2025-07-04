import mysql.connector

config = {
    'host' : 'localhost',
    'port' : '3306',
    #'database' : 'crypto_data',
    'user' : 'root',
    'password' : '1234567'
}

try:
    conn = mysql.connector.connect(**config)
    print("Connected to MySQL database", conn.server_info)

    cursor = conn.cursor()
    
    #show all database
    cursor.execute("SHOW DATABASES")
    print("\n database:")
    for db in cursor:
        print("-", db[0])

#cursor.execute("CREATE DATABASE IF NOT EXISTS my_app_db")
#print("Created database 'my_app_db'")

        
except mysql.connector.Error as err:
    print("\n error:", err)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()


