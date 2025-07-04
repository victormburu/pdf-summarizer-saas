# 🛒 Fake Store API to MySQL

This Python script fetches product data from the [Fake Store API](https://fakestoreapi.com/products), creates a MySQL database and table (if they don't exist), and stores the products data. It also displays the fetched data on the console and verifies database insertion.

## 📦 Features

- Connects to the [Fake Store API](https://fakestoreapi.com/)
- Creates a MySQL database and table if not already present
- Inserts or updates product records with duplicate ID handling
- Displays fetched data in the console
- Prints all product titles and categories stored in MySQL

## 🧱 Table Schema

```sql
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
````

## 🚀 Setup Instructions

### 1. Prerequisites

* Python 3.x
* MySQL Server
* `requests` and `mysql-connector-python` libraries

### 2. Install Required Python Packages

```bash
pip install requests mysql-connector-python
```

### 3. Clone the Repository

```bash
git clone https://github.com/your-username/fake-store-api-mysql.git
cd fake-store-api-mysql
```

### 4. Update Your MySQL Credentials

Inside the script, update your MySQL configuration:

```python
config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'your_password'
}
```

### 5. Run the Script

```bash
python fetch_and_store.py
```

## 📊 Sample Output

```
ID: 1
Title: Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops
Price: $109.95
Category: men's clothing
Rating: 3.9 stars (120 reviews)
------------------------------------------------------------
Connected to store_data database
Data inserted successfully
Current data in database:
Title: Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops, Category: men's clothing
...
```

## 🧠 Author

Victor Mburu
Python Developer | Data Enthusiast | BI Learner

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
