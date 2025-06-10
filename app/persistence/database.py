# app/persistence/database.py
import time
import mysql.connector
from mysql.connector import pooling
from app.core.config import settings

connection_pool = None

def init_db_with_retries():
    """
    Initializes the database connection pool with a retry mechanism
    to handle the race condition on startup.
    """
    global connection_pool
    retries = 10
    delay = 3  # seconds

    for i in range(retries):
        try:
            print(f"Database connection attempt {i + 1}/{retries}...")
            connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
            print("Database connection pool initialized successfully.")
            return
        except mysql.connector.Error as err:
            print(f"Connection failed: {err}. Retrying in {delay} seconds...")
            time.sleep(delay)

    raise Exception("Could not connect to the database after several retries.")

def create_tables():
    """Creates the 'users' table if it doesn't exist."""
    if connection_pool is None:
        raise RuntimeError("Database pool is not initialized.")

    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        print("Creating table 'users' if it does not exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        ) ENGINE=InnoDB;
        """)
        connection.commit()
        print("Table 'users' is ready.")
    finally:
        cursor.close()
        connection.close()

# --- Run initialization immediately when this module is imported ---
init_db_with_retries()
create_tables()