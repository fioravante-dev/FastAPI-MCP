import time
import mysql.connector
from mysql.connector import pooling
from app.core.config import settings

def init_db_with_retries():
    """
    Initializes and returns a database connection pool with a retry mechanism.
    """
    retries = 10
    delay = 3
    for i in range(retries):
        try:
            print(f"Database connection attempt {i + 1}/{retries}...")
            pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
            print("Database connection pool initialized successfully.")
            return pool
        except mysql.connector.Error as err:
            print(f"Connection failed: {err}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Could not connect to the database after several retries.")

connection_pool = init_db_with_retries()

def create_tables():
    """Creates the required tables if they don't exist."""
    if connection_pool is None:
        raise RuntimeError("Database pool is not initialized.")
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        # Create users table
        print("Creating table 'users' if it does not exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        ) ENGINE=InnoDB;
        """)
        print("Table 'users' is ready.")
        
        # Create agents table
        print("Creating table 'agents' if it does not exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
        """)
        print("Table 'agents' is ready.")
        
        # Create employees table
        print("Creating table 'employees' if it does not exist...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id VARCHAR(255) PRIMARY KEY,
            company_name TEXT NOT NULL,
            full_name TEXT NOT NULL,
            admission_date DATE NOT NULL,
            termination_date DATE,
            status_description TEXT NOT NULL,
            birth_date DATE,
            cost_center_name TEXT NOT NULL,
            salary DECIMAL(10,2) NOT NULL,
            complementary_salary DECIMAL(10,2),
            salary_effective_date DATE,
            gender CHAR(1) NOT NULL,
            street_address TEXT,
            address_number TEXT,
            city_name TEXT,
            race TEXT,
            postal_code TEXT,
            company_cod_senior_numemp INT,
            employee_cod_senior_numcad INT,
            collaborator_type_code_senior_tipcol INT,
            status_cod_senior_sitafa INT,
            cost_center_cod_senior_codccu INT,
            agent_id INT NOT NULL,
            FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)
        print("Table 'employees' is ready.")
        
        # Insert default agent if it doesn't exist
        print("Checking for default agent...")
        cursor.execute("SELECT COUNT(*) FROM agents WHERE id = 1")
        agent_count = cursor.fetchone()[0]
        
        if agent_count == 0:
            print("Creating default agent...")
            cursor.execute("""
            INSERT INTO agents (id, name, description) 
            VALUES (1, 'Default Agent', 'Default agent for employee management')
            """)
            print("Default agent created with ID 1.")
        else:
            print("Default agent already exists.")
        
        connection.commit()
        print("All tables and default data are ready.")
    finally:
        cursor.close()
        connection.close()

# Create tables immediately after the pool is initialized.
create_tables()