import requests
import mysql.connector

#fetch api data
url = "https://fakestoreapi.com/products"
r = requests.get(url)
products = r.json()

#display data
for product in products:
    print(f"ID: {product['id']}")
    print(f"Title: {product['title']}")
    print(f"Price: ${product['price']}")
    print(f"Category: {product['category']}")
    print(f"Rating: {product['rating']['rate']} stars ({product['rating']['count']} reviews)")
    print('-' * 60)

db_name = 'store_data'
config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': '1234567'
}

conn = None
cursor = None

try:
    #Connect without specifying database to create it if needed
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()
    conn.close()

    #Now connect to the database
    config['database'] = db_name
    conn = mysql.connector.connect(**config)
    print(f"Connected to {db_name} database")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            price DECIMAL(10, 2),
            category VARCHAR(100),
            description TEXT,
            image TEXT,
            rating_rate FLOAT,
            rating_count INT
        );
    """)

    #Inserting data
    for product in products:
        cursor.execute("""
            INSERT INTO products (id, title, price, category, description, image, rating_rate, rating_count)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            title=VALUES(title),
            price=VALUES(price),
            category=VALUES(category),
            description=VALUES(description),
            image=VALUES(image),
            rating_rate=VALUES(rating_rate),
            rating_count=VALUES(rating_count);
        """, (
            product['id'],
            product['title'],
            product['price'],
            product['category'],
            product['description'],
            product['image'],
            product['rating']['rate'],
            product['rating']['count']
        ))
    conn.commit()
    print("Data inserted successfully")

    # After inserting data and before closing the connection
    cursor.execute("SELECT title, category FROM products")
    rows = cursor.fetchall()
    print("Current data in database:")
    for row in rows:
        print(f"Title: {row[0]}, Category: {row[1]}")
except mysql.connector.Error as err:
    print("\nError:", err)

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None and conn.is_connected():
        conn.close()







