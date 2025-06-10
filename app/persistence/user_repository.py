from typing import List, Tuple, Optional
from app.persistence.database import connection_pool

def list_all() -> List[Tuple[str, str]]:
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT name, email FROM users")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add(name: str, email: str):
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        # Use %s placeholders for security (prevents SQL injection)
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def get_by_name(name: str) -> Optional[Tuple[str, str]]:
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True) # Get results as dicts
    try:
        query = "SELECT name, email FROM users WHERE name = %s"
        cursor.execute(query, (name,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def update(name: str, new_name: Optional[str], new_email: Optional[str]) -> int:
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        query_parts = []
        params = []
        if new_name:
            query_parts.append("name = %s")
            params.append(new_name)
        if new_email:
            query_parts.append("email = %s")
            params.append(new_email)

        params.append(name)
        query = f"UPDATE users SET {', '.join(query_parts)} WHERE name = %s"
        cursor.execute(query, tuple(params))
        connection.commit()
        return cursor.rowcount # Returns the number of rows affected
    finally:
        cursor.close()
        connection.close()

def delete(name: str) -> int:
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM users WHERE name = %s"
        cursor.execute(query, (name,))
        connection.commit()
        return cursor.rowcount # Returns the number of rows affected
    finally:
        cursor.close()
        connection.close()