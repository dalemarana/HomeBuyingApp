import os

CONTENT_FOLDER = "home_buying_app/Content"
os.makedirs(CONTENT_FOLDER, exist_ok=True)

# Default Content for Output PDF
TOC = [            
    "1. Title Page",
    "2. Executive Summary",
    "3. Methodology",
    "4. User Inputs",
    "5. Expense Analysis",
    "6. Rent vs Mortgage Payments as % of Income",
    "7. Non-Recoverable Cost Analysis",
    "8. Opportunity Cost Analysis",
    "9. Conclusion",
    ]

EXECUTIVE_SUMMARY = """
    This report provides a comprehensive analysis of the financial implications of buying a home 
    compared to renting. Key metrics include estimated mortgage payments, cumulative costs, 
    and equity growth over time. The analysis highlights the potential financial benefits 
    and trade-offs associated with homeownership compared to renting and investing shown thru
    Non-Recoverable Cost Analysis and Opportunity cost Analysis.
    """

METHODOLOGY = """
    Calculations in this report are based on standard financial formulas and assumptions:
        - Mortgage payments are calculated using the loan amount, interest rate, and term.
        - Rent vs mortgage comparison incorporates rent inflation and income growth rates.
        - Equity growth considers property appreciation and principal repayment.
        - Stock Growth rate considers the appreciation and money invested to the stock market.
            This is considered by getting the balance of mortgage payment and rent, then investing
            the balance.
    All data provided by the client is assumed to be accurate.
    """

DISCLAIMER = """
        This report is for informational purposes only. Calculations are based on estimates and 
        assumptions provided by the client. Actual financial outcomes may vary due to changes in 
        market conditions, interest rates, or other factors.
    """

