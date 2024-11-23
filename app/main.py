from fastapi import FastAPI, HTTPException

from app.schemas import Customer

app = FastAPI()

# In-memory data store
customers = {}


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Customer API"}


@app.post("/customers/", response_model=Customer)
async def create_customer(customer: Customer):
    if customer.id in customers:
        raise HTTPException(status_code=400, detail="Customer already exists")
    customers[customer.id] = customer
    return customer


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    customer = customers.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.delete("/customers/{customer_id}", response_model=Customer)
async def delete_customer(customer_id: int):
    customer = customers.pop(customer_id, None)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
