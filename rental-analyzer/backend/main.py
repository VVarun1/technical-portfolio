from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class PropertyParams(BaseModel):
    price: float
    down_payment: float
    interest_rate: float
    term_years: int
    monthly_rent: float
    monthly_expenses: float
    vacancy_rate: float

def calculate_metrics(p: PropertyParams):
    loan_amount = p.price - p.down_payment
    monthly_rate = p.interest_rate / 100 / 12
    num_payments = p.term_years * 12
    
    # Mortgage Payment (Amortization Formula)
    monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    net_operating_income = (p.monthly_rent * (1 - p.vacancy_rate)) - p.monthly_expenses
    annual_noi = net_operating_income * 12
    
    cash_flow = net_operating_income - monthly_mortgage
    annual_cash_flow = cash_flow * 12
    
    cap_rate = (annual_noi / p.price) * 100
    cash_on_cash = (annual_cash_flow / p.down_payment) * 100
    
    return {
        "monthly_mortgage": monthly_mortgage,
        "annual_noi": annual_noi,
        "annual_cash_flow": annual_cash_flow,
        "cap_rate": cap_rate,
        "cash_on_cash": cash_on_cash
    }

@app.post("/analyze")
async def analyze(params: PropertyParams):
    return calculate_metrics(params)
