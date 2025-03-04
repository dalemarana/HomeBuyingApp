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
A) Using the GUI
	1.	Ensure you have all dependencies installed:
```
pip install -r requirements.txt
```

	2.	Run the application:
```
python main.py
```

	3.	The graphical interface will open, allowing you to input data and generate results.

B) Importing processing.py for Custom Use

Developers can integrate the core logic into their own applications by importing processing.py. Example:
```
from processing import calculate_mortgage, analyze_expenses

# Example usage:
loan_amount = 250000
rate = 4.5
years = 30

monthly_payment = calculate_mortgage(loan_amount, rate, years)
print(f"Monthly Payment: {monthly_payment}")

# Example expense analysis
data = load_config()  # Load configurations if needed
analysis = analyze_expenses(data)
print(analysis)
```
4. View the generated financial report and conclusions.

## Questions and Comments
For any inquiries, suggestions, or issues, please contact us via email:
📧 **support@homebuyingtool.com**

