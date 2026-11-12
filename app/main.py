from fastapi import FastAPI, HTTPException, Response

from schemas import Employee, EmployeeCreate, EmployeeUpdate

app = FastAPI()

employees: dict[int, Employee] = {}
next_id = 1


def get_or_404(employee_id: int) -> Employee:
    employee = employees.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/employees", response_model=Employee, status_code=201)
async def create_employee(payload: EmployeeCreate):
    global next_id
    employee = Employee(id=next_id, **payload.model_dump())
    employees[next_id] = employee
    next_id += 1
    return employee


@app.get("/employees", response_model=list[Employee])
async def list_employees(department: str | None = None):
    result = list(employees.values())
    if department:
        result = [e for e in result if e.department == department]
    return result


@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int):
    return get_or_404(employee_id)


@app.put("/employees/{employee_id}", response_model=Employee)
async def replace_employee(employee_id: int, payload: EmployeeCreate):
    get_or_404(employee_id)
    employee = Employee(id=employee_id, **payload.model_dump())
    employees[employee_id] = employee
    return employee


@app.patch("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, payload: EmployeeUpdate):
    existing = get_or_404(employee_id)
    changes = payload.model_dump(exclude_unset=True)
    updated = Employee(**{**existing.model_dump(), **changes})
    employees[employee_id] = updated
    return updated


@app.delete("/employees/{employee_id}", status_code=204)
async def delete_employee(employee_id: int):
    get_or_404(employee_id)
    del employees[employee_id] 
    return Response(status_code=204)