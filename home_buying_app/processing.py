import logging

# # Configure logging
# logging.basicConfig(
#     filename="logs/home_buying.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

def process_data(values):
    """Processes input values and returns structured financial data."""

    try:
        # print(values)

        name = values.get("name", "Joe")
        age = int(values.get("age", "33"))
        occupation = values.get("occupation", "Engineer")
        status = values.get("status", "Married")
        residence = values.get("residence", "Apartment")

        annual_income = float(values.get("annual_income", 90000))
        monthly_income = float(values.get("monthly_income", 5200))

        rent = float(values.get("rent", 1475))
        electricity = float(values.get("electricity", 90))
        water = float(values.get("water", 25))
        groceries = float(values.get("groceries", 250))
        council_tax = float(values.get("council_tax", 170))
        other = float(values.get("other", 200))

        property_value = float(values.get("property_value", 440000))
        deposit = float(values.get("deposit", 44000))
        duration = int(values.get("duration", 33))
        solicitor = float(values.get("solicitor", 3250))
        survey = float(values.get("survey", 750))
        furnishings = float(values.get("furnishings", 3000))

        inflation = float(values.get("inflation", 2.0))
        interest_rate = float(values.get("interest_rate", 5.4))
        rent_inflation = float(values.get("rent_inflation", 4.0))
        income_growth = float(values.get("income_growth", 2.5))
        property_growth = float(values.get("property_growth", 4.0))
        property_tax_rate = float(values.get("property_tax_rate", 0.0))
        discount_rate = float(values.get("discount_rate", 3.0))
        maintenance_rate = float(values.get("maintenance_rate", 1.0))
        stock_growth_rate = float(values.get("stock_growth_rate", 7.7))


        # Expense Cost Calculation

        rent_expenses, needs_expenses_costs, wants_expenses_costs, remaining_income_rent, remaining_income_mortgage, mortgage, remaining_income_rent_pv, remaining_income_mortgage_pv = generate_expense_cost(property_value, deposit, rent, duration, property_tax_rate, maintenance_rate, interest_rate, rent_inflation, discount_rate, income_growth, inflation, electricity, water, groceries, council_tax, other, monthly_income)

        # Non-Recoverable Cost Calculation
        homeownership_costs, renting_costs, yearly_differences, homeownership_costs_pv, renting_costs_pv = generate_non_recoverable_cost(property_value, deposit, rent, duration, property_tax_rate, maintenance_rate, interest_rate, rent_inflation, discount_rate)


        nonrecoverable_cost_difference = homeownership_costs_pv - renting_costs_pv
        # print(f"Present Value Difference: {nonrecoverable_cost_difference}\n\n")
        # print(f"Present_value: {pv_difference}")

        # Opportunity Cost Calculation
        home_equity_growth, stock_investment_growth, yearly_differences = generate_opportunity_cost(property_value, deposit, rent, duration, property_tax_rate, maintenance_rate, interest_rate, rent_inflation, stock_growth_rate, property_growth)

        years = len(home_equity_growth)
        home_equity_pv = home_equity_growth[years - 1] / ((1 + (discount_rate / 100)) ** (years - 1))
        # print(f"Home Equity PV: {home_equity_pv}\n")

        stock_investment_pv = stock_investment_growth[years - 1] / ((1 + (discount_rate / 100)) ** (years - 1))
        # print(f"Stock Investment PV: {stock_investment_pv}\n")

        opportunity_cost_difference = home_equity_pv - stock_investment_pv
        # print(f"Present Value Difference: {opportunity_cost_difference}")

        logging.info("Processing complete.")
        return {
                "user_details" : [
                    {
                        "name": name,
                        "age": age,
                        "occupation": occupation,
                        "status": status,
                    },
                    {
                        "annual_income": annual_income,
                        "monthly_income": monthly_income,
                    },
                    {
                        "property_value": property_value,
                        "deposit": deposit,
                        "monthly_mortgage_payment": mortgage[0],
                        "mortgage_rate": interest_rate,
                    },
                    {
                        "rent_inflation": rent_inflation,
                        "income_growth": income_growth,
                        "property_growth": property_growth,
                        "property_tax_rate": property_tax_rate,
                        "maintenance_rate": maintenance_rate,
                        "stock_growth_rate": stock_growth_rate,
                    }
                ],
                "expense_cost_analysis": [{
                    "duration": duration,
                    "rent_expenses": rent_expenses,
                    "needs_expenses_costs": needs_expenses_costs,
                    "wants_expenses_costs": wants_expenses_costs,
                    "remaining_income_rent": remaining_income_rent,
                    "remaining_income_mortgage": remaining_income_mortgage,
                    "mortgage": mortgage,
                    "remaining_income_rent_pv": remaining_income_rent_pv,
                    "remaining_income_mortgage_pv": remaining_income_mortgage_pv,
                }],
                "non_recoverable_costs":[{
                    "homeownership_costs": homeownership_costs,
                    "renting_costs": renting_costs,
                    "nonrecoverable_cost_difference": nonrecoverable_cost_difference,
                    "homeownership_costs_pv": homeownership_costs_pv,
                    "renting_costs_pv": renting_costs_pv,
                }],
                "opportunity_costs":[{
                    "home_equity_growth": home_equity_growth,
                    "stock_investment_growth": stock_investment_growth,
                    "opportunity_cost_difference": opportunity_cost_difference,
                    "home_equity_pv": home_equity_pv,
                    "stock_investment_pv": stock_investment_pv,
                }],
            }

    except Exception as e:
        logging.error(f"Processing error: {e}")


def calculate_mortgage_payment(property_value, deposit, interest_rate, duration):
    """
    Calculates the monthly mortgage payment based on user-provided data.
    
    :param property_value: The value of the property.
    :param deposit: The deposit amount.
    :param values: Dictionary of user input values containing interest rate and term details.
    :return: Monthly mortgage payment.
    """

    try:
        # Loan principal (property value minus deposit)
        loan_amount = property_value - deposit
        
        # Interest rate and term
        interest_rate = interest_rate / 100

        duration = duration  # Fixed mortgage term (in years)

        # Monthly interest rate
        monthly_interest_rate = interest_rate / 12

        # Total number of payments
        total_payments = duration * 12


        # Monthly payment calculation (Amortization formula)
        monthly_payment = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments / \
                        ((1 + monthly_interest_rate) ** total_payments - 1)
        
        # print(monthly_payment)
        # sg.popup(f"Monthly Mortgage Payment: £{monthly_payment:.2f}")
        return monthly_payment

    except Exception as e:
        logging.error(f"Error calculating mortgage payment: {e}")
        return 0


def generate_non_recoverable_cost(property_value, deposit, rent, duration, property_tax_rate, 
    maintenance_rate, interest_rate, rent_inflation, discount_rate):

    # Lists to store costs for each year
    homeownership_costs = []
    renting_costs = []
    yearly_differences = []

    try:
        annual_mortgage_payment = calculate_mortgage_payment(property_value, deposit, interest_rate, duration) * 12
        current_annual_rent = rent * 12
        remaining_loan = property_value - deposit
        

        # Calculate yearly non-recoverable costs
        for _ in range(1, duration + 1):
            # Non-recoverable costs for homeownership
            annual_interest_cost = remaining_loan * (interest_rate / 100)
            annual_property_tax = property_value * (property_tax_rate / 100)
            maintenance_cost = maintenance_rate * (maintenance_rate / 100)

            annual_homeownership_cost = annual_property_tax + maintenance_cost + annual_interest_cost

            # Reduce the remaining loan by the principal paid this year
            principal_paid = annual_mortgage_payment - annual_interest_cost
            remaining_loan = max(remaining_loan - principal_paid, 0) # Prevent negative loan values

            # Non-recoverable costs for renting (with inflation)
            annual_rent_cost = current_annual_rent
            current_annual_rent *= (1 + (rent_inflation / 100))

            # Append Costs
            homeownership_costs.append(annual_homeownership_cost)
            renting_costs.append(annual_rent_cost)

            # Difference
            yearly_differences.append(annual_homeownership_cost - annual_rent_cost)


        # Calculate the present value (PV) difference
        # discount_rate = float(values.get('discount_rate', 3)) / 100  # Use a default discount rate of 3% if not provided
        # pv_difference = sum(diff / ((1 + discount_rate) ** year) for year, diff in enumerate(yearly_differences, start=1))
        # pv_difference = yearly_differences[len(yearly_differences) - 1] / ((1 + (discount_rate / 100)) ** years)
        # print(pv_difference)
        homeownership_costs_pv = present_value(homeownership_costs, discount_rate)
        renting_costs_pv = present_value(renting_costs, discount_rate)

        return homeownership_costs, renting_costs, yearly_differences, homeownership_costs_pv, renting_costs_pv
    
    except Exception as e:
        logging.error(f"Error calculating Non-Recoverable cost: {e}")
        return None, None, None, None


def generate_opportunity_cost(property_value, deposit, rent, duration, property_tax_rate, 
    maintenance_rate, interest_rate, rent_inflation, stock_growth_rate, property_growth):
    """Function to calculate yearly opportunity costs"""

    # Lists to store values for each year
    home_equity_growth = []
    stock_investment_growth = []
    yearly_differences = []

    try:

        annual_mortgage_payment = calculate_mortgage_payment(property_value, deposit, interest_rate, duration) * 12
        current_annual_rent = rent * 12
        remaining_loan = property_value - deposit

        equity = deposit
        stock_investment = deposit

        # Simulate yearly growth
        for _ in range(1, duration + 1):
            # Update rent based on inflation
            current_annual_rent *= (1 + (rent_inflation / 100))

            # Principal paid this year
            annual_interest = remaining_loan * (interest_rate / 100)
            # print(f"Current Annual Interest: {annual_interest}")
            principal_paid = annual_mortgage_payment - annual_interest
            remaining_loan = max(0, remaining_loan - principal_paid)

            # Update home equity
            equity += principal_paid # Add principal payments
            equity *= (1 + (property_growth / 100))  # Add property growth
            home_equity_growth.append(equity)

            # Yearly difference for investment
            difference = max(0, annual_mortgage_payment - current_annual_rent)
            stock_investment += difference
            stock_investment *= (1 + (stock_growth_rate / 100))
            stock_investment_growth.append(stock_investment)
            # print(stock_investment)
            yearly_differences.append(equity - stock_investment)

        
        return home_equity_growth, stock_investment_growth, yearly_differences

    except Exception as e:
        logging.error(f"Error calculating opportunity cost: {e}")
        return None, None, None
    pass


def generate_expense_cost(property_value, deposit, rent, duration, property_tax_rate, maintenance_rate, interest_rate, rent_inflation, discount_rate, income_growth, inflation,
    electricity, water, groceries, council_tax, other, monthly_income):
    """
    Generate expense analysis for renting and homeownership scenarios.
    Inflation is applied to all recurring expenses.
    """

    # Initialize arrays for expenses and remaining income
    needs_expenses_costs = []
    wants_expenses_costs = []
    remaining_income_rent = []
    remaining_income_mortgage = []
    mortgage = []


    try:
        yearly_income = monthly_income * 12
        rent_expenses = generate_non_recoverable_cost(property_value, deposit, rent, duration, property_tax_rate, maintenance_rate, interest_rate, rent_inflation, discount_rate)[1]
        mortgage_payment = calculate_mortgage_payment(property_value, deposit, interest_rate, duration)

        needs_expenses = (electricity + water + groceries + council_tax) * 12
        wants_expenses = other * 12

        # Calculate Remaining income after expenses
        for year in range(1, duration + 1):
            # Update Income
            yearly_income *= (1 + (income_growth / 100))

            # Update Rent
            current_rent = float(rent_expenses[year - 1])

            # Current Mortgage
            current_mortgage = mortgage_payment * 12

            # Apply inflation to expenses
            needs_expenses *= (1 + (inflation / 100))
            needs_expenses_costs.append(needs_expenses)

            wants_expenses *= (1 + (inflation / 100))
            wants_expenses_costs.append(wants_expenses)

            total_expenses = needs_expenses + wants_expenses

            current_remaining_income_rent = yearly_income - (current_rent + total_expenses)
            current_remaining_income_mortgage = yearly_income - (current_mortgage + total_expenses)

            mortgage.append(current_mortgage)
            # Remaining income after expenses
            remaining_income_rent.append(current_remaining_income_rent)
            remaining_income_mortgage.append(current_remaining_income_mortgage)


        remaining_income_rent_pv = present_value(remaining_income_rent, discount_rate)
        remaining_income_mortgage_pv = present_value(remaining_income_mortgage, discount_rate)

        # print(remaining_income_rent_pv, remaining_income_mortgage_pv)
        # logging.info("Expense analysis generated successfully!")
        return rent_expenses, needs_expenses_costs, wants_expenses_costs, remaining_income_rent, remaining_income_mortgage, mortgage, remaining_income_rent_pv, remaining_income_mortgage_pv

    except Exception as e:
        logging.error(f"Error calculating expense analysis: {e}")
        return None, None, None, None

    pass


def present_value(yearly_values, discount_rate):
    pv = 0
    for i, value in enumerate(yearly_values):
        pv += value / ((1 + (discount_rate / 100)) ** (1 + i))
    
    return pv
