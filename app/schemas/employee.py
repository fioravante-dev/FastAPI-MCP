from pydantic import BaseModel, Field
from typing import Optional, Literal

class GetEmployeeDetailsInput(BaseModel):
    employee_id: str = Field(description="The employee ID to search for.")

class GetEmployeeDetailsByNameInput(BaseModel):
    full_name: str = Field(description="The full name of the employee to search for.")

class GetEmployeesByCompanyInput(BaseModel):
    company_name: str = Field(description="The company name to search employees for.")

class GetEmployeesByStatusInput(BaseModel):
    status_description: str = Field(description="The status description to filter employees by.")

class GetEmployeesByCostCenterInput(BaseModel):
    cost_center_name: str = Field(description="The cost center name to filter employees by.")

class GetEmployeeSalaryInfoInput(BaseModel):
    employee_id: str = Field(description="The employee ID to get salary information for.")

class GetEmployeesByDateRangeInput(BaseModel):
    start_date: str = Field(description="Start date for filtering (YYYY-MM-DD format).")
    end_date: str = Field(description="End date for filtering (YYYY-MM-DD format).")
    date_type: str = Field(description="Type of date to filter by: 'admission', 'termination', or 'birth'.")

class GetDistinctValuesInput(BaseModel):
    dimension: Literal["company_name", "city_name", "cost_center_name", "race", "gender", "status_description"] = Field(
        ...,
        description="The dimension or column to analyze. Must be one of: company_name, city_name, cost_center_name, race, gender, status_description."
    )
