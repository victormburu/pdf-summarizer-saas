from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector.errors import Error
from typing import Dict, List, Optional
import logging
from contextlib import contextmanager

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(livename)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Handles all database operations with connection pooling"""
    
    def __init__(self, config: Dict):
        self.pool = self._create_pool(config)
        
    def create_pool(self, config: Dict) -> MySQLConnectionPool:
        """Initialize connection pool with validation"""
        try:
            return MySQLConnectionPool(
                pool_name=config.get('pool_name', 'bizbot_pool'),
                pool_size=config.get('pool_size', 5),
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                ssl_disabled=not config.get('ssl', False),
                autocommit=config.get('commit', False),
                charset=config.get('charset', 'utf8mb4'),
                connect_timeout= config.get('connect_timeout', 30),
                collation=config.get('collation', 'utf8mb4_unicode_ci')
            )
        except Error as e:
            logger.critical(f"Failed to create connection pool: {str(e)}")
            raise

    @contextmanager
    def _get_cursor(self, dictionary: bool = False):
        """Context manager for safe cursor handling"""
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary=dictionary)
        try:
            yield cursor
            conn.commit()
        except Error as e:
            conn.rollback()
            logger.error(f"Database operation failed: {str(e)}")
            raise
        finally:
            cursor.close()
            conn.close()

    def fetch_products(self, category: Optional[str] = None) -> List[Dict]:
        """Get products with optional category filter"""
        with self._get_cursor(dictionary=True) as cursor:
            if category:
                cursor.execute(
                    "SELECT id, name, price, stock, unit FROM products WHERE category = %s",
                    (category.lower(),)
                )
            else:
                cursor.execute("SELECT id, name, price, stock, unit FROM products")
            return cursor.fetchall()

    def place_order(self, customer_id: int, product_id: int, quantity: int) -> Dict:
        """Process order with inventory check in transaction"""
        with self._get_cursor() as cursor:
            try:
                # Verify product and lock row
                cursor.execute(
                    """SELECT name, price, stock FROM products 
                    WHERE id = %s FOR UPDATE""",
                    (product_id,)
                )
                product = cursor.fetchone()
                
                if not product:
                    raise ValueError("Product not found")
                    
                name, price, stock = product
                
                # Validate stock
                if stock < quantity:
                    raise ValueError(f"Insufficient stock. Available: {stock}")
                
                # Create order
                cursor.execute(
                    """INSERT INTO orders 
                    (customer_id, product_id, quantity, unit_price, product_name, status)
                    VALUES (%s, %s, %s, %s, %s, 'pending')""",
                    (customer_id, product_id, quantity, price, name)
                )
                order_id = cursor.lastrowid
                
                # Update inventory
                cursor.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (quantity, product_id)
                )
                
                return {
                    'order_id': order_id,
                    'product': name,
                    'quantity': quantity,
                    'total': price * quantity
                }
                
            except Error as e:
                logger.error(f"Order failed: {str(e)}")
                raise ValueError(f"Order processing error: {str(e)}")

    def get_order_history(self, customer_id: int, limit: int = 10) -> List[Dict]:
        """Retrieve customer's recent orders"""
        with self._get_cursor(dictionary=True) as cursor:
            cursor.execute(
                """SELECT o.id, o.quantity, o.unit_price, o.status, o.order_date,
                p.name as product_name, p.category 
                FROM orders o JOIN products p ON o.product_id = p.id
                WHERE customer_id = %s ORDER BY o.order_date DESC LIMIT %s""",
                (customer_id, limit)
            )
            return cursor.fetchall()

    def update_order(self, order_id: int, **updates) -> bool:
        """Update order attributes"""
        if not updates:
            return False
            
        with self._get_cursor() as cursor:
            set_clause = ", ".join(f"{k} = %s" for k in updates)
            values = list(updates.values())
            values.append(order_id)
            
            cursor.execute(
                f"UPDATE orders SET {set_clause} WHERE id = %s",
                values
            )
            return cursor.rowcount > 0