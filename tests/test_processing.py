import pytest
from processing import (
    process_data,
    calculate_mortgage_payment,
    generate_non_recoverable_cost,
    generate_opportunity_cost,
    generate_expense_cost,
    present_value,
)

# Sample input data for testing
TEST_INPUT = {
    "name": "Dale Marana",
    "age": "33",
    "occupation": "Software Engineer",
    "status": "Married",
    "residence": "United Kingdom",
    "currency": "GBP",
    "annual_income": "90000",
    "monthly_income": "5200",
    "rent": "1475",
    "electricity": "90",
    "water": "25",
    "groceries": "250",
    "council_tax": "170",
    "other": "200",
    "property_value": "440000",
    "deposit": "44000",
    "duration": "33",
    "inflation": "2.5",
    "interest_rate": "4.9",
    "rent_inflation": "4.0",
    "income_growth": "2.5",
    "property_growth": "4.0",
    "property_tax_rate": "0.0",
    "discount_rate": "3.0",
    "maintenance_rate": "1.0",
    "stock_growth_rate": "7.7",
}

# 🔹 Test process_data()
def test_process_data():
    result = process_data(TEST_INPUT)
    assert result is not None
    assert "user_details" in result
    assert result["user_details"][0]["name"] == "Dale Marana"
    assert result["user_details"][1]["annual_income"] == 90000.0
    assert result["expense_cost_analysis"][0]["rent_expenses"] is not None

# 🔹 Test calculate_mortgage_payment()
@pytest.mark.parametrize(
    "property_value, deposit, interest_rate, duration, expected_min, expected_max",
    [
        (440000, 44000, 4.9, 33, 2000, 2500),  # Expected range in GBP
        (440000, 44000, 5.4, 33, 1500, 2200),
    ],
)
def test_calculate_mortgage_payment(property_value, deposit, interest_rate, duration, expected_min, expected_max):
    result = calculate_mortgage_payment(property_value, deposit, interest_rate, duration)
    assert expected_min <= result <= expected_max

# 🔹 Test generate_non_recoverable_cost()
def test_generate_non_recoverable_cost():
    costs = generate_non_recoverable_cost(500000, 50000, 2000, 30, 1.2, 1.0, 4.5, 3.0, 3.5)
    assert costs is not None
    assert all(costs)  # Ensure no None values
    assert len(costs[0]) == 30  # 30-year duration

# 🔹 Test generate_opportunity_cost()
def test_generate_opportunity_cost():
    equity_growth, stock_growth, differences = generate_opportunity_cost(500000, 50000, 2000, 30, 1.2, 1.0, 4.5, 3.0, 7.0, 5.0)
    assert len(equity_growth) == 30
    assert len(stock_growth) == 30
    assert len(differences) == 30

# 🔹 Test generate_expense_cost()
def test_generate_expense_cost():
    result = generate_expense_cost(500000, 50000, 2000, 30, 1.2, 1.0, 4.5, 3.0, 3.5, 2.0, 2.5, 100, 30, 500, 200, 300, 10000)
    assert len(result[0]) == 30  # Rent expenses
    assert len(result[1]) == 30  # Needs expenses
    assert len(result[2]) == 30  # Wants expenses

# 🔹 Test present_value()
def test_present_value():
    values = [1000] * 30  # $1000 per year for 30 years
    result = present_value(values, 3.5)  
    assert result > 0
    assert result < sum(values)  # PV should be lower than total