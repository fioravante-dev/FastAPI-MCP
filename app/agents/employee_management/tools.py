import mysql.connector
from langchain_core.tools import tool
from app.persistence import employee_repository
from app.schemas.employee import (
    GetEmployeeDetailsInput, GetEmployeesByCompanyInput, GetEmployeesByStatusInput, 
    GetEmployeesByCostCenterInput, GetEmployeeSalaryInfoInput, GetEmployeesByDateRangeInput, 
    GetEmployeeDetailsByNameInput, GetDistinctValuesInput
)

@tool
def list_active_employees() -> str:
    """Lists all active employees (those without termination date)."""
    employees = employee_repository.get_active_employees()
    if not employees:
        return "There are no active employees in the database."
    
    result = []
    for emp in employees:
        result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Company: {emp['company_name']}, Cost Center: {emp['cost_center_name']})")
    
    return "\n".join(result)

@tool
def list_terminated_employees() -> str:
    """Lists all terminated employees (those with termination date)."""
    employees = employee_repository.get_terminated_employees()
    if not employees:
        return "There are no terminated employees in the database."
    
    result = []
    for emp in employees:
        result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Terminated: {emp['termination_date']})")
    
    return "\n".join(result)

@tool("get_employee_details", args_schema=GetEmployeeDetailsInput)
def get_employee_details(employee_id: str) -> str:
    """Finds a specific employee by their employee ID and returns detailed information."""
    employee = employee_repository.get_by_employee_id(employee_id=employee_id)
    if not employee:
        return f"No employee found with ID '{employee_id}'."
    
    status = "TERMINATED" if employee.get('termination_date') else "ACTIVE"
    result = f"""Employee Details:
    - ID: {employee['employee_id']}
    - Name: {employee['full_name']}
    - Company: {employee['company_name']}
    - Status: {status}
    - Admission Date: {employee['admission_date']}
    - Cost Center: {employee['cost_center_name']}
    - Salary: ${employee['salary']:,.2f}"""
    
    if employee.get('complementary_salary'):
        result += f"\n- Complementary Salary: ${employee['complementary_salary']:,.2f}"
    
    if employee.get('termination_date'):
        result += f"\n- Termination Date: {employee['termination_date']}"
    
    if employee.get('birth_date'):
        result += f"\n- Birth Date: {employee['birth_date']}"
    
    if employee.get('city_name'):
        result += f"\n- City: {employee['city_name']}"
    
    return result

@tool("get_employees_by_company", args_schema=GetEmployeesByCompanyInput)
def get_employees_by_company(company_name: str) -> str:
    """Gets all employees from a specific company."""
    employees = employee_repository.get_by_company(company_name=company_name)
    if not employees:
        return f"No employees found for company '{company_name}'."
    
    result = [f"Employees at {company_name}:"]
    for emp in employees:
        status = " (TERMINATED)" if emp.get('termination_date') else " (ACTIVE)"
        result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}){status}")
    
    return "\n".join(result)

@tool("get_employees_by_status", args_schema=GetEmployeesByStatusInput)
def get_employees_by_status(status_description: str) -> str:
    """Gets all employees with a specific status description."""
    employees = employee_repository.get_by_status(status_description=status_description)
    if not employees:
        return f"No employees found with status '{status_description}'."
    
    result = [f"Employees with status '{status_description}':"]
    for emp in employees:
        result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Company: {emp['company_name']})")
    
    return "\n".join(result)

@tool("get_employees_by_cost_center", args_schema=GetEmployeesByCostCenterInput)
def get_employees_by_cost_center(cost_center_name: str) -> str:
    """Gets all employees from a specific cost center."""
    employees = employee_repository.get_by_cost_center(cost_center_name=cost_center_name)
    if not employees:
        return f"No employees found in cost center '{cost_center_name}'."
    
    result = [f"Employees in cost center '{cost_center_name}':"]
    for emp in employees:
        status = " (TERMINATED)" if emp.get('termination_date') else " (ACTIVE)"
        result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Company: {emp['company_name']}){status}")
    
    return "\n".join(result)

@tool("get_employee_salary_info", args_schema=GetEmployeeSalaryInfoInput)
def get_employee_salary_info(employee_id: str) -> str:
    """Gets salary information for a specific employee."""
    salary_info = employee_repository.get_salary_info(employee_id=employee_id)
    if not salary_info:
        return f"No employee found with ID '{employee_id}'."
    
    result = f"""Salary Information for {salary_info['full_name']}:
    - Employee ID: {salary_info['employee_id']}
    - Base Salary: ${salary_info['salary']:,.2f}
    - Cost Center: {salary_info['cost_center_name']}"""
    
    if salary_info.get('complementary_salary'):
        total_salary = salary_info['salary'] + salary_info['complementary_salary']
        result += f"\n- Complementary Salary: ${salary_info['complementary_salary']:,.2f}"
        result += f"\n- Total Salary: ${total_salary:,.2f}"
    
    if salary_info.get('salary_effective_date'):
        result += f"\n- Salary Effective Date: {salary_info['salary_effective_date']}"
    
    return result

@tool("get_employees_by_date_range", args_schema=GetEmployeesByDateRangeInput)
def get_employees_by_date_range(start_date: str, end_date: str, date_type: str) -> str:
    """Gets employees filtered by date range for admission, termination, or birth dates."""
    try:
        employees = employee_repository.get_by_date_range(
            start_date=start_date, end_date=end_date, date_type=date_type
        )
        if not employees:
            return f"No employees found with {date_type} date between {start_date} and {end_date}."
        
        result = [f"Employees with {date_type} date between {start_date} and {end_date}:"]
        for emp in employees:
            date_value = emp.get(f'{date_type}_date', 'N/A')
            result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Date: {date_value})")
        
        return "\n".join(result)
    except ValueError as e:
        return f"Error: {str(e)}"

@tool("get_employee_by_name", args_schema=GetEmployeeDetailsByNameInput)
def get_employee_by_name(full_name: str) -> str:
    """Finds employees by their full name or part of their name and returns complete detailed information."""
    employees = employee_repository.get_by_name(full_name=full_name)
    if not employees:
        return f"No employee found with name containing '{full_name}'."
    
    if len(employees) == 1:
        employee = employees[0]
        status = "TERMINATED" if employee.get('termination_date') else "ACTIVE"
        result = f"""Complete Employee Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 BASIC INFORMATION:
- Employee ID: {employee['employee_id']}
- Full Name: {employee['full_name']}
- Company: {employee['company_name']}
- Employment Status: {status}
- Gender: {employee.get('gender', 'N/A')}
- Birth Date: {employee.get('birth_date', 'N/A')}
- Race: {employee.get('race', 'N/A')}

💼 EMPLOYMENT DETAILS:
- Admission Date: {employee['admission_date']}
- Cost Center: {employee['cost_center_name']}
- Status Description: {employee['status_description']}"""
        
        if employee.get('termination_date'):
            result += f"\n- Termination Date: {employee['termination_date']}"
        
        result += f"\n\n💰 SALARY INFORMATION:"
        result += f"\n- Base Salary: ${employee['salary']:,.2f}"
        
        if employee.get('complementary_salary') and employee['complementary_salary'] > 0:
            total_salary = employee['salary'] + employee['complementary_salary']
            result += f"\n- Complementary Salary: ${employee['complementary_salary']:,.2f}"
            result += f"\n- Total Monthly Salary: ${total_salary:,.2f}"
            result += f"\n- Annual Salary (Base): ${employee['salary'] * 12:,.2f}"
            result += f"\n- Annual Salary (Total): ${total_salary * 12:,.2f}"
        else:
            result += f"\n- Annual Salary: ${employee['salary'] * 12:,.2f}"
        
        if employee.get('salary_effective_date'):
            result += f"\n- Salary Effective Date: {employee['salary_effective_date']}"
        
        result += f"\n\n🏠 ADDRESS INFORMATION:"
        if employee.get('street_address'):
            address = employee['street_address']
            if employee.get('address_number'):
                address += f", {employee['address_number']}"
            result += f"\n- Address: {address}"
        else:
            result += f"\n- Address: N/A"
        
        result += f"\n- City: {employee.get('city_name', 'N/A')}"
        result += f"\n- Postal Code: {employee.get('postal_code', 'N/A')}"
        
        # Technical codes section
        result += f"\n\n🔧 SYSTEM CODES:"
        result += f"\n- Company Code: {employee.get('company_cod_senior_numemp', 'N/A')}"
        result += f"\n- Employee Code: {employee.get('employee_cod_senior_numcad', 'N/A')}"
        result += f"\n- Collaborator Type Code: {employee.get('collaborator_type_code_senior_tipcol', 'N/A')}"
        result += f"\n- Status Code: {employee.get('status_cod_senior_sitafa', 'N/A')}"
        result += f"\n- Cost Center Code: {employee.get('cost_center_cod_senior_codccu', 'N/A')}"
        result += f"\n- Agent ID: {employee.get('agent_id', 'N/A')}"
        
        return result
    else:
        # Multiple employees found
        result = [f"Found {len(employees)} employees with name containing '{full_name}':"]
        result.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for i, emp in enumerate(employees, 1):
            status = "TERMINATED" if emp.get('termination_date') else "ACTIVE"
            result.append(f"{i}. {emp['full_name']}")
            result.append(f"   • ID: {emp['employee_id']}")
            result.append(f"   • Company: {emp['company_name']}")
            result.append(f"   • Status: {status}")
            result.append(f"   • Cost Center: {emp['cost_center_name']}")
            result.append(f"   • Salary: ${emp['salary']:,.2f}")
            if emp.get('termination_date'):
                result.append(f"   • Terminated: {emp['termination_date']}")
            result.append("")
        
        result.append("💡 To get complete details for a specific employee, search with their exact name or use their Employee ID.")
        return "\n".join(result)

@tool(return_direct=True)
def greet_employee_manager() -> str:
    """Provides a greeting and explains the employee management agent's capabilities."""
    return """Hello! I am an employee database assistant. I can help you with:

📊 **Employee Information & Search:**
- List active employees or terminated employees
- Search employees by ID or name (full name or partial name)
- Get complete detailed information for any employee

🏢 **Filtering & Organization:**
- Find employees by company
- Filter by employment status or cost center
- Search by date ranges (admission, termination, birth dates)

💰 **Salary Information:**
- Get detailed salary breakdowns
- View base salary, complementary salary, and totals
- Calculate annual salary amounts

🔍 **Advanced Search:**
- Search by partial names (e.g., "John" will find "John Smith")
- Filter employees by various criteria
- Get comprehensive employee profiles

📈 **Data Analysis:**
- Get distinct value counts and lists for dimensions like:
  • Companies, cities, cost centers
  • Employee races, genders, status descriptions
- Answer questions like "How many companies are there?" or "List all unique cities"

⚠️ **Important:** Due to the large database size, I only provide filtered searches. Please specify criteria like name, company, or status rather than requesting all employees.

Just ask me what you'd like to know about the employees!"""

@tool("get_distinct_values_summary", args_schema=GetDistinctValuesInput)
def get_distinct_values_summary(dimension: str) -> str:
    """
    Calculates the total count of unique values for a given dimension and lists them.
    Use this tool to answer questions like 'How many distinct companies are there and what are their names?' 
    or 'List all unique cities present in the employee data'.
    The 'dimension' parameter must be one of the following: 'company_name', 'city_name', 'cost_center_name', 'race', 'gender', 'status_description'.
    """
    
    # Define allowed dimensions for security
    allowed_dimensions = ['company_name', 'city_name', 'cost_center_name', 'race', 'gender', 'status_description']
    
    if dimension not in allowed_dimensions:
        return f"Error: Analysis of dimension '{dimension}' is not permitted or does not exist."

    try:
        # Get the count of distinct values
        distinct_count = employee_repository.count_distinct(column=dimension)
        
        # Get the list of distinct values
        distinct_values = employee_repository.list_distinct(column=dimension)

        if distinct_count == 0:
            return f"No distinct values found for the dimension '{dimension}'."

        # Format the result clearly
        result = [
            f"📊 Summary for dimension: '{dimension.replace('_', ' ').title()}'",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"Total unique values found: {distinct_count}\n"
        ]

        # Limit display to avoid overwhelming output if there are thousands of values
        limit = 100
        if distinct_count > limit:
            result.append(f"Showing the first {limit} unique values (sorted alphabetically):")
        else:
            result.append("List of unique values:")
        
        result.extend([f"- {value}" for value in distinct_values[:limit]])

        if distinct_count > limit:
            result.append(f"\n...and {distinct_count - limit} more.")
            
        return "\n".join(result)

    except Exception as e:
        return f"An error occurred while analyzing the dimension '{dimension}'. Please check if the dimension is correct and try again."

@tool("error_response", args_schema=GetEmployeeDetailsInput)
def error_response(error_message: str) -> str:
    """Returns a user-friendly error message when the AI cannot perform a requested task."""
    return f"❌ I'm not able to perform that task. {error_message}\n\nI can help you with:\n• Searching for employees by name, ID, company, or status\n• Getting detailed employee information\n• Filtering employees by various criteria\n• Providing salary information\n\nPlease let me know how else I can assist you!"
