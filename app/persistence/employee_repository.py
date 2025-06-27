from typing import List, Tuple, Optional, Dict, Any
from app.persistence.database import connection_pool

def list_all() -> List[Dict[str, Any]]:
    """Get all employees from the database."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employees")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_by_employee_id(employee_id: str) -> Optional[Dict[str, Any]]:
    """Get employee by employee ID."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def get_by_company(company_name: str) -> List[Dict[str, Any]]:
    """Get all employees from a specific company."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE company_name = %s"
        cursor.execute(query, (company_name,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_by_status(status_description: str) -> List[Dict[str, Any]]:
    """Get all employees with a specific status."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE status_description = %s"
        cursor.execute(query, (status_description,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_by_cost_center(cost_center_name: str) -> List[Dict[str, Any]]:
    """Get all employees from a specific cost center."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE cost_center_name = %s"
        cursor.execute(query, (cost_center_name,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_by_date_range(start_date: str, end_date: str, date_type: str) -> List[Dict[str, Any]]:
    """Get employees filtered by date range for admission, termination, or birth dates."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if date_type == 'admission':
            query = "SELECT * FROM employees WHERE admission_date BETWEEN %s AND %s"
        elif date_type == 'termination':
            query = "SELECT * FROM employees WHERE termination_date BETWEEN %s AND %s"
        elif date_type == 'birth':
            query = "SELECT * FROM employees WHERE birth_date BETWEEN %s AND %s"
        else:
            raise ValueError("Invalid date_type. Use 'admission', 'termination', or 'birth'")
        
        cursor.execute(query, (start_date, end_date))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_salary_info(employee_id: str) -> Optional[Dict[str, Any]]:
    """Get salary-related information for a specific employee."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT employee_id, full_name, salary, complementary_salary, 
               salary_effective_date, cost_center_name 
        FROM employees WHERE employee_id = %s
        """
        cursor.execute(query, (employee_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def add(employee_data: Dict[str, Any]):
    """Add a new employee to the database."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        # Build the INSERT query dynamically based on provided fields
        fields = list(employee_data.keys())
        placeholders = ', '.join(['%s'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO employees ({field_names}) VALUES ({placeholders})"
        values = tuple(employee_data.values())
        
        cursor.execute(query, values)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def update(employee_id: str, update_data: Dict[str, Any]) -> int:
    """Update an existing employee's information."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        # Remove None values from update_data
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not update_data:
            return 0
        
        query_parts = []
        params = []
        
        for field, value in update_data.items():
            query_parts.append(f"{field} = %s")
            params.append(value)
        
        params.append(employee_id)
        query = f"UPDATE employees SET {', '.join(query_parts)} WHERE employee_id = %s"
        
        cursor.execute(query, tuple(params))
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()

def delete(employee_id: str) -> int:
    """Delete an employee from the database."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM employees WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()

def get_active_employees() -> List[Dict[str, Any]]:
    """Get all employees who don't have a termination date (active employees)."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE termination_date IS NULL"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_terminated_employees() -> List[Dict[str, Any]]:
    """Get all employees who have a termination date (terminated employees)."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE termination_date IS NOT NULL"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_by_name(full_name: str) -> List[Dict[str, Any]]:
    """Get employees by full name (can return multiple matches)."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees WHERE full_name LIKE %s"
        cursor.execute(query, (f"%{full_name}%",))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def count_distinct(column: str) -> int:
    """Get the count of distinct values for a specified column."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        # Use parameterized query to prevent SQL injection
        allowed_columns = ['company_name', 'city_name', 'cost_center_name', 'race', 'gender', 'status_description']
        if column not in allowed_columns:
            raise ValueError(f"Column '{column}' is not allowed for distinct analysis")
        
        query = f"SELECT COUNT(DISTINCT {column}) FROM employees WHERE {column} IS NOT NULL"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        connection.close()

def list_distinct(column: str, limit: int = 100) -> List[str]:
    """Get a list of distinct values for a specified column."""
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    try:
        # Use parameterized query to prevent SQL injection
        allowed_columns = ['company_name', 'city_name', 'cost_center_name', 'race', 'gender', 'status_description']
        if column not in allowed_columns:
            raise ValueError(f"Column '{column}' is not allowed for distinct analysis")
        
        query = f"SELECT DISTINCT {column} FROM employees WHERE {column} IS NOT NULL ORDER BY {column} LIMIT %s"
        cursor.execute(query, (limit,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()
