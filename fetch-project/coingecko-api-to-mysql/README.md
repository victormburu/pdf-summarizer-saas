# Fetch-data
## Crypto Data Analysis Project Report

### Project Overview
This project demonstrates a complete pipeline for fetching cryptocurrency market data from an API, storing it in a MySQL database, and performing analysis using SQL queries. The system tracks real-time cryptocurrency prices, market caps, and other metrics.

### Technical Stack
- **Database**: MySQL 8.0.42 Community Server
- **Programming Language**: Python
- **Database Interface**: MySQL Connector/Python
- **API**: CoinMarketCap (or similar cryptocurrency API)

### Database Structure
**Database Name**: `crypto_data`  
**Table Name**: `crypto`  

| Column       | Type          | Description                |
|--------------|---------------|----------------------------|
| name         | VARCHAR(255)  | Cryptocurrency name        |
| symbol       | VARCHAR(20)   | Trading symbol             |
| price        | DECIMAL(20,10)| Current price in USD       |
| market_cap   | BIGINT        | Market capitalization      |

### Key Operations Demonstrated
1. **Database & Table Creation**
   ```sql
   CREATE DATABASE crypto_data;
   USE crypto_data;
   
   CREATE TABLE crypto (
       name VARCHAR(255),
       symbol VARCHAR(20),
       price DECIMAL(18,8),
       market_cap BIGINT
   );
   ```

2. **Data Import** (from Python API)
   ```python
   import mysql.connector
   import requests
   
   # Fetch data from API
   response = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing')
   crypto_data = response.json()['data']['cryptoCurrencyList']
   
   # Connect to MySQL
   conn = mysql.connector.connect(
       host='localhost',
       user='root',
       password='1234567',
       database='crypto_data'
   )
   
   # Insert data
   cursor = conn.cursor()
   for coin in crypto_data:
       cursor.execute(
           "INSERT INTO crypto (name, symbol, price, market_cap) VALUES (%s, %s, %s, %s)",
           (coin['name'], coin['symbol'], coin['quote']['USD']['price'], coin['quote']['USD']['market_cap'])
       )
   conn.commit()
   ```

3. **SQL Operations Performed**
   ```sql
   -- Top 5 cryptocurrencies
   SELECT * FROM crypto LIMIT 5;
   
   -- Cryptocurrencies over $10,000
   SELECT * FROM crypto WHERE price > 10000;
   
   -- Rank by price (descending)
   SELECT * FROM crypto ORDER BY price DESC;
   
   -- Count total records
   SELECT COUNT(*) FROM crypto;
   
   -- Schema modifications
   ALTER TABLE crypto MODIFY COLUMN price DECIMAL(20,10);
   ALTER TABLE crypto ADD COLUMN volume BIGINT;
   ALTER TABLE crypto DROP COLUMN volume;
   ```

### Key Insights from Data
1. **Market Dominance**:
   - Bitcoin dominates with price (~$109,837) and market cap ($2.18T)
   - Ethereum follows with $2,590 price and $312B market cap

2. **Stablecoins**:
   - Tether (USDT) and USDC maintain $1.00 peg
   - Combined market cap over $220B

3. **Performance Highlights**:
   ```sql
   -- Top 5 by market cap
   SELECT name, price, market_cap 
   FROM crypto 
   ORDER BY market_cap DESC 
   LIMIT 5;
   ```
   | name      | price       | market_cap     |
   |-----------|-------------|----------------|
   | Bitcoin   | 109837.0000 | 2183696052858  |
   | Ethereum  |  2590.0400  | 312634065831   |
   | Tether    |     1.0000  | 158327682245   |
   | XRP       |     2.2800  | 134640043723   |
   | BNB       |   661.2500  |  96442480351   |

### Challenges & Solutions
1. **Connection Issues**:
   - *Problem*: Host parameter misconfigured as port number
   - *Solution*: Corrected to `host='localhost'` and `port=3306`

2. **Schema Modifications**:
   - *Problem*: Syntax errors in ALTER TABLE commands
   - *Solution*: Standardized SQL syntax and verified table existence

3. **Data Precision**:
   - *Problem*: Insufficient decimal precision for crypto prices
   - *Solution*: Expanded to `DECIMAL(20,10)`
   ```sql
   ALTER TABLE crypto MODIFY COLUMN price DECIMAL(20,10);
   ```

### Next Steps
1. Implement automated hourly data refreshes
2. Add historical price tracking table
3. Develop visualization dashboard (Tableau/Power BI)
4. Set up user authentication system
5. Add volatility analysis and price prediction models

### GitHub Repository Structure
```
/crypto-data-project
├── data_ingestion.py      # API fetching and DB insertion
├── database_utils.py      # DB connection manager
├── queries.sql            # Sample SQL queries
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

This project demonstrates a functional pipeline for cryptocurrency data acquisition and analysis. The solution can be extended to create a comprehensive cryptocurrency tracking and analysis platform.
