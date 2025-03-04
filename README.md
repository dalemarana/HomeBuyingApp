# Home Buying Analysis Tool
![Python CI](https://github.com/dalemarana/HomeBuyingApp/actions/workflows/python-ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/dalemarana/HomeBuyingApp/branch/main/graph/badge.svg)

## Introduction
The Home Buying Analysis Tool is a comprehensive financial analysis program designed to help individuals compare the financial implications of buying a home versus renting. By analyzing key financial factors such as mortgage payments, rent costs, opportunity costs, and non-recoverable expenses, this tool provides users with insights to make informed housing decisions.

## Features
- **Expense Cost Analysis:** Compare mortgage payments and rent expenses over time.
- **Non-Recoverable Cost Evaluation:** Assess the impact of homeownership costs versus renting costs.
- **Opportunity Cost Calculation:** Analyze potential gains from stock investments versus home equity growth.
- **Present Value Computation:** Evaluate future financial values in today’s terms for better comparison.
- **Customizable Inputs:** Users can adjust income growth, property value appreciation, mortgage rates, and other economic variables.
- **Detailed Conclusion:** The tool generates a clear, data-driven summary to assist decision-making.

## How to Use
**A) Using the GUI**

	1.	Ensure you have all dependencies installed:
    
``` python
pip install -r requirements.txt
```

	2.	Then run the application, and the graphical interface will open, allowing you to input data and generate results:

``` python
python main.py
```

**B) Importing processing.py for Custom Use**

Developers can integrate the core logic into their own applications by importing processing.py. 
Example:
```
from home_buying_app.processing import process_data, calculate_mortgage_payment
from home_buying_app.output import generate_graphs_and_report

# Example usage:
loan_amount = 250000
deposit = 50000
rate = 4.5
years = 30

monthly_payment = calculate_mortgage(loan_amount, deposit, rate, years)
print(f"Monthly Payment: {monthly_payment}")


# Example Processing data and Generating a report

data = {
    'name': 'John Doe', 'age': '33', 'occupation': 'Engineer', 'status': 'Married', 'residence': 'United Kingdom', 'annual_income': '90000', 'monthly_income': '5200', 'rent': '1475', 'electricity': '90', 'water': '25', 'groceries': '250', 'council_tax': '170', 'other': '200', 'property_value': '440000', 'deposit': '44000', 'duration': '33', 'solicitor': '3250', 'survey': '750', 'furnishings': '3000', 'inflation': 2.0, 'interest_rate': 5.4, 'rent_inflation': 4.0, 'income_growth': 2.5, 'property_growth': 4.0, 'property_tax_rate': 0.0, 'discount_rate': 3.0, 'maintenance_rate': 1.0, 'stock_growth_rate': 7.7, 'TabGroup': '-TAB6-', 'Inflation, consumer prices (%)': 6.79, 'Interest Rate (%)': None, 'currency': 'GBP', 'exchange_rate_to_usd': 0.7948
}

processed_data = process_data(data)

# User Details
print(processed_data["user_details"])

# Expense Cost Analysis
print(processed_data["expense_cost_analysis"])

# Non Recoverable Costs
print(processed_data["non_recoverable_costs"])

# Opportunity Costs
print(processed_data["opportunity_costs"])

# Generating Graphs and Report
filename = generate_graphs_and_report(processed_data)

```
4. View the generated financial report and conclusions.

## Questions and Comments
For any inquiries, suggestions, or issues, please contact us via email:
📧 **dalemarana@gmail.com**

