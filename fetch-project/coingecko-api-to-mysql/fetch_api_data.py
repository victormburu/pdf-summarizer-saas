import requests  # Import the requests library to make HTTP requests
import mysql.connector  # Import the MySQL connector library to interact with MySQL databases

# Fetch data from API
url = 'https://api.coingecko.com/api/v3/coins/markets'  # API endpoint for fetching cryptocurrency market data
params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 50}  # Parameters for the API request: USD currency, order by market cap, top 50 coins
r = requests.get(url, params=params)  # Send GET request to the API with the specified parameters
data = r.json()  # Parse the JSON response from the API into a Python object

db_name = 'crypto_data'  # Name of the database to use or create
config = {
    'host': 'localhost',  # Database host (local machine)
    'port': '3306',  # MySQL default port
    'user': 'root',  # MySQL username
    'password': '1234567'  # MySQL password
}

conn = None  # Initialize connection variable
cursor = None  # Initialize cursor variable

try:
    # Connect without specifying database to create it if needed
    conn = mysql.connector.connect(**config)  # Connect to MySQL server (no database yet)
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")  # Create the database if it doesn't exist
    cursor.close()  # Close the cursor after creating the database
    conn.close()  # Close the connection after creating the database

    # Now connect to the database
    config['database'] = db_name  # Add the database name to the config
    conn = mysql.connector.connect(**config)  # Connect to the specific database
    print(f"Connected to {db_name} database")  # Print confirmation of connection
    cursor = conn.cursor()  # Create a new cursor for the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto (
            name VARCHAR(255),  # Name of the cryptocurrency
            symbol VARCHAR(20),  # Symbol (e.g., BTC, ETH)
            price DECIMAL(18, 8),  # Current price with high precision
            market_cap BIGINT  # Market capitalization
        );
    """)  # Create the crypto table if it doesn't exist
    # Insert data
    for coin in data:  # Loop through each coin in the API data
        cursor.execute(
            "INSERT INTO crypto (name, symbol, price, market_cap) VALUES (%s, %s, %s, %s)",  # SQL insert statement
            (coin['name'], coin['symbol'], coin['current_price'], coin['market_cap'])  # Insert coin data into table
        )
    conn.commit()  # Commit the transaction to save changes
    print("Data inserted successfully")  # Print confirmation of data insertion

    # After inserting data and before closing the connection
    cursor.execute("SELECT name, price FROM crypto")  # Select name and price from the crypto table
    rows = cursor.fetchall()  # Fetch all rows from the query
    print("Current data in database:")  # Print header for output
    for row in rows:  # Loop through each row
        print(f"Name: {row[0]}, Price: {row[1]}")  # Print the name and price of each coin
except mysql.connector.Error as err:
    print("\nError:", err)  # Print any MySQL errors that occur
finally:
    if cursor is not None:
        cursor.close()  # Ensure the cursor is closed
    if conn is not None and conn.is_connected():
        conn.close()  # Ensure the connection is closed