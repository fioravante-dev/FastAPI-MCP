import mysql.connector
from langchain_core.tools import tool
from app.persistence import employee_repository
from app.schemas.employee import (
    GetEmployeeDetailsInput, AddEmployeeInput, UpdateEmployeeInput, DeleteEmployeeInput,
    GetEmployeesByCompanyInput, GetEmployeesByStatusInput, GetEmployeesByCostCenterInput,
    GetEmployeeSalaryInfoInput, GetEmployeesByDateRangeInput, GetEmployeeDetailsByNameInput
)


@tool
def list_all_employees() -> str:
    """Lists all employees currently in the database."""
    employees = employee_repository.list_all()
    if not employees:
        return "There are no employees in the database."
    
    result = []
    for emp in employees:
        status = " (TERMINATED)" if emp.get('termination_date') else " (ACTIVE)"
        result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Company: {emp['company_name']}){status}")
    
    return "\n".join(result)

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

@tool("add_new_employee", args_schema=AddEmployeeInput)
def add_new_employee(
    employee_id: str, company_name: str, full_name: str, admission_date: str,
    status_description: str, cost_center_name: str, salary: float, gender: str,
    agent_id: int, termination_date: str = None, birth_date: str = None,
    complementary_salary: float = None, salary_effective_date: str = None,
    street_address: str = None, address_number: str = None, city_name: str = None,
    race: str = None, postal_code: str = None, company_cod_senior_numemp: int = None,
    employee_cod_senior_numcad: int = None, collaborator_type_code_senior_tipcol: int = None,
    status_cod_senior_sitafa: int = None, cost_center_cod_senior_codccu: int = None
) -> str:
    """Adds a new employee to the database."""
    try:
        # Build employee data dictionary, excluding None values for optional fields
        employee_data = {
            'employee_id': employee_id,
            'company_name': company_name,
            'full_name': full_name,
            'admission_date': admission_date,
            'status_description': status_description,
            'cost_center_name': cost_center_name,
            'salary': salary,
            'gender': gender,
            'agent_id': agent_id
        }
        
        # Add optional fields if provided
        optional_fields = {
            'termination_date': termination_date,
            'birth_date': birth_date,
            'complementary_salary': complementary_salary,
            'salary_effective_date': salary_effective_date,
            'street_address': street_address,
            'address_number': address_number,
            'city_name': city_name,
            'race': race,
            'postal_code': postal_code,
            'company_cod_senior_numemp': company_cod_senior_numemp,
            'employee_cod_senior_numcad': employee_cod_senior_numcad,
            'collaborator_type_code_senior_tipcol': collaborator_type_code_senior_tipcol,
            'status_cod_senior_sitafa': status_cod_senior_sitafa,
            'cost_center_cod_senior_codccu': cost_center_cod_senior_codccu
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                employee_data[field] = value
        
        employee_repository.add(employee_data=employee_data)
        return f"Employee '{full_name}' (ID: {employee_id}) was successfully added."
    except mysql.connector.IntegrityError:
        return f"Error: An employee with ID '{employee_id}' already exists."

@tool("update_employee_details", args_schema=UpdateEmployeeInput)
def update_employee_details(
    employee_id: str, company_name: str = None, full_name: str = None,
    admission_date: str = None, termination_date: str = None,
    status_description: str = None, birth_date: str = None,
    cost_center_name: str = None, salary: float = None,
    complementary_salary: float = None, salary_effective_date: str = None,
    gender: str = None, street_address: str = None, address_number: str = None,
    city_name: str = None, race: str = None, postal_code: str = None,
    company_cod_senior_numemp: int = None, employee_cod_senior_numcad: int = None,
    collaborator_type_code_senior_tipcol: int = None, status_cod_senior_sitafa: int = None,
    cost_center_cod_senior_codccu: int = None, agent_id: int = None
) -> str:
    """Modifies the details of an existing employee."""
    # Build update data dictionary, excluding None values
    update_data = {}
    all_fields = {
        'company_name': company_name,
        'full_name': full_name,
        'admission_date': admission_date,
        'termination_date': termination_date,
        'status_description': status_description,
        'birth_date': birth_date,
        'cost_center_name': cost_center_name,
        'salary': salary,
        'complementary_salary': complementary_salary,
        'salary_effective_date': salary_effective_date,
        'gender': gender,
        'street_address': street_address,
        'address_number': address_number,
        'city_name': city_name,
        'race': race,
        'postal_code': postal_code,
        'company_cod_senior_numemp': company_cod_senior_numemp,
        'employee_cod_senior_numcad': employee_cod_senior_numcad,
        'collaborator_type_code_senior_tipcol': collaborator_type_code_senior_tipcol,
        'status_cod_senior_sitafa': status_cod_senior_sitafa,
        'cost_center_cod_senior_codccu': cost_center_cod_senior_codccu,
        'agent_id': agent_id
    }
    
    for field, value in all_fields.items():
        if value is not None:
            update_data[field] = value
    
    if not update_data:
        return "Error: You must provide at least one field to update."
    
    try:
        rows_affected = employee_repository.update(
            employee_id=employee_id, update_data=update_data
        )
        if rows_affected == 0:
            return f"Error: No employee found with ID '{employee_id}' to update."
        return f"Successfully updated employee with ID '{employee_id}'."
    except mysql.connector.IntegrityError:
        return f"Error: Update failed due to constraint violation (duplicate ID or invalid reference)."

@tool("delete_employee", args_schema=DeleteEmployeeInput)
def delete_employee(employee_id: str) -> str:
    """Permanently deletes an existing employee."""
    rows_affected = employee_repository.delete(employee_id=employee_id)
    if rows_affected == 0:
        return f"Error: No employee found with ID '{employee_id}' to delete."
    return f"Employee with ID '{employee_id}' has been successfully deleted."

@tool("get_employee_by_name", args_schema=GetEmployeeDetailsByNameInput)
def get_employee_by_name(full_name: str) -> str:
    """Finds a specific employee by their full name and returns detailed information."""
    employees = employee_repository.get_by_name(full_name=full_name)
    if not employees:
        return f"No employee found with name '{full_name}'."
    
    if len(employees) == 1:
        employee = employees[0]
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
        
        if employee.get('gender'):
            result += f"\n- Gender: {employee['gender']}"
        
        return result
    else:
        # Multiple employees with same name
        result = [f"Found {len(employees)} employees with name '{full_name}':"]
        for emp in employees:
            status = " (TERMINATED)" if emp.get('termination_date') else " (ACTIVE)"
            result.append(f"- {emp['full_name']} (ID: {emp['employee_id']}, Company: {emp['company_name']}){status}")
        result.append("\nPlease use the employee ID to get specific details.")
        return "\n".join(result)

@tool(return_direct=True)
def greet_employee_manager() -> str:
    """Provides a greeting and explains the employee management agent's capabilities."""
    return """Hello! I am an employee database management assistant. I can help you with:

📊 **Listing & Searching:**
- List all employees, active employees, or terminated employees
- Search employees by ID, company, status, or cost center
- Filter employees by date ranges (admission, termination, birth dates)

💰 **Salary Information:**
- Get detailed salary information for specific employees
- View base salary, complementary salary, and totals

👥 **Employee Management:**
- Add new employees with comprehensive details
- Update existing employee information
- Delete employee records

🔍 **Advanced Queries:**
- Find employees by various criteria
- Get company-specific employee lists
- Filter by employment status or cost centers

Just ask me what you'd like to do with the employee database!"""
