from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class GetEmployeeDetailsInput(BaseModel):
    employee_id: str = Field(description="The employee ID to search for.")

class GetEmployeesByCompanyInput(BaseModel):
    company_name: str = Field(description="The company name to search employees for.")

class GetEmployeesByStatusInput(BaseModel):
    status_description: str = Field(description="The status description to filter employees by.")

class GetEmployeesByCostCenterInput(BaseModel):
    cost_center_name: str = Field(description="The cost center name to filter employees by.")

class AddEmployeeInput(BaseModel):
    employee_id: str = Field(description="Unique employee identifier.")
    company_name: str = Field(description="The company name.")
    full_name: str = Field(description="The full name of the employee.")
    admission_date: str = Field(description="Employee admission date (YYYY-MM-DD format).")
    status_description: str = Field(description="Current employment status description.")
    cost_center_name: str = Field(description="Cost center name.")
    salary: float = Field(description="Base salary amount.")
    gender: str = Field(description="Employee gender (M/F/O).")
    agent_id: int = Field(description="Associated agent ID.")
    termination_date: Optional[str] = Field(default=None, description="Termination date if applicable (YYYY-MM-DD format).")
    birth_date: Optional[str] = Field(default=None, description="Birth date (YYYY-MM-DD format).")
    complementary_salary: Optional[float] = Field(default=None, description="Additional salary amount.")
    salary_effective_date: Optional[str] = Field(default=None, description="Salary effective date (YYYY-MM-DD format).")
    street_address: Optional[str] = Field(default=None, description="Street address.")
    address_number: Optional[str] = Field(default=None, description="Address number.")
    city_name: Optional[str] = Field(default=None, description="City name.")
    race: Optional[str] = Field(default=None, description="Employee race/ethnicity.")
    postal_code: Optional[str] = Field(default=None, description="Postal code.")
    company_cod_senior_numemp: Optional[int] = Field(default=None, description="Company senior code.")
    employee_cod_senior_numcad: Optional[int] = Field(default=None, description="Employee senior code.")
    collaborator_type_code_senior_tipcol: Optional[int] = Field(default=None, description="Collaborator type code.")
    status_cod_senior_sitafa: Optional[int] = Field(default=None, description="Status senior code.")
    cost_center_cod_senior_codccu: Optional[int] = Field(default=None, description="Cost center senior code.")

class UpdateEmployeeInput(BaseModel):
    employee_id: str = Field(description="The employee ID to update.")
    company_name: Optional[str] = Field(default=None, description="New company name.")
    full_name: Optional[str] = Field(default=None, description="New full name.")
    admission_date: Optional[str] = Field(default=None, description="New admission date (YYYY-MM-DD format).")
    termination_date: Optional[str] = Field(default=None, description="New termination date (YYYY-MM-DD format).")
    status_description: Optional[str] = Field(default=None, description="New status description.")
    birth_date: Optional[str] = Field(default=None, description="New birth date (YYYY-MM-DD format).")
    cost_center_name: Optional[str] = Field(default=None, description="New cost center name.")
    salary: Optional[float] = Field(default=None, description="New base salary.")
    complementary_salary: Optional[float] = Field(default=None, description="New complementary salary.")
    salary_effective_date: Optional[str] = Field(default=None, description="New salary effective date (YYYY-MM-DD format).")
    gender: Optional[str] = Field(default=None, description="New gender (M/F/O).")
    street_address: Optional[str] = Field(default=None, description="New street address.")
    address_number: Optional[str] = Field(default=None, description="New address number.")
    city_name: Optional[str] = Field(default=None, description="New city name.")
    race: Optional[str] = Field(default=None, description="New race/ethnicity.")
    postal_code: Optional[str] = Field(default=None, description="New postal code.")
    company_cod_senior_numemp: Optional[int] = Field(default=None, description="New company senior code.")
    employee_cod_senior_numcad: Optional[int] = Field(default=None, description="New employee senior code.")
    collaborator_type_code_senior_tipcol: Optional[int] = Field(default=None, description="New collaborator type code.")
    status_cod_senior_sitafa: Optional[int] = Field(default=None, description="New status senior code.")
    cost_center_cod_senior_codccu: Optional[int] = Field(default=None, description="New cost center senior code.")
    agent_id: Optional[int] = Field(default=None, description="New agent ID.")

class DeleteEmployeeInput(BaseModel):
    employee_id: str = Field(description="The employee ID to delete.")

class GetEmployeeSalaryInfoInput(BaseModel):
    employee_id: str = Field(description="The employee ID to get salary information for.")

class GetEmployeesByDateRangeInput(BaseModel):
    start_date: str = Field(description="Start date for filtering (YYYY-MM-DD format).")
    end_date: str = Field(description="End date for filtering (YYYY-MM-DD format).")
    date_type: str = Field(description="Type of date to filter by: 'admission', 'termination', or 'birth'.")

class GetEmployeeDetailsByNameInput(BaseModel):
    full_name: str = Field(description="The full name of the employee to search for.")
