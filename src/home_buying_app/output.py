import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import use
import numpy as np
import os
import logging
from fpdf import FPDF
from datetime import datetime
from home_buying_app.content import TOC, EXECUTIVE_SUMMARY, METHODOLOGY, DISCLAIMER

use('TkAgg')

REPORTS_FOLDER = f"{os.getcwd()}/home_buying_app/Reports"
os.makedirs(REPORTS_FOLDER, exist_ok=True)

RENTING_GRAPH_PATH = f"{REPORTS_FOLDER}/Graphs/renting_expenses.png"
OWNERSHIP_GRAPH_PATH = f"{REPORTS_FOLDER}/Graphs/homeownership_expenses.png"
NON_RECOVERABLE_COSTS_GRAPH_PATH = f"{REPORTS_FOLDER}/Graphs/non_recoverable_cost_analysis.png"
OPPORTUNITY_COST_GRAPH_PATH = f"{REPORTS_FOLDER}/Graphs/opportunity_cost_analysis.png"
SUMMARY_GRAPH = f"{REPORTS_FOLDER}/Graphs/summary.png"



def generate_graphs_and_report(data):
    """Generates expense graphs and saves a summary PDF report."""

    try:
        # print(data)
        
        os.makedirs(f"{REPORTS_FOLDER}/Graphs", exist_ok=True)
        duration = data["expense_cost_analysis"][0]["duration"]
        years_range = range(1, duration + 1)
        currency = data["user_details"][0]["currency"]


        # Rent vs Mortgage Expenses Graph
        rent_expenses = data["expense_cost_analysis"][0]["rent_expenses"]
        needs_expenses_costs = data["expense_cost_analysis"][0]["needs_expenses_costs"]
        wants_expenses_costs = data["expense_cost_analysis"][0]["wants_expenses_costs"]
        remaining_income_rent = data["expense_cost_analysis"][0]["remaining_income_rent"]
        remaining_income_mortgage = data["expense_cost_analysis"][0]["remaining_income_mortgage"]
        mortgage_payment = data["expense_cost_analysis"][0]["mortgage"]


        # Plotting Rent Scenario
        plt.figure(figsize=(10, 6))
        # years_range = range(1, years + 1)
        plt.bar(years_range, rent_expenses, label='Rent', color='skyblue', edgecolor="black", alpha=0.7)
        plt.bar(years_range, needs_expenses_costs, bottom=rent_expenses, label='Needs', color='lightgreen', edgecolor="black", alpha=0.7)
        plt.bar(years_range, wants_expenses_costs, bottom=[r + n for r, n in zip(rent_expenses, needs_expenses_costs)], label='Wants', color='lightcoral', edgecolor="black", alpha=0.7)
        plt.bar(years_range, remaining_income_rent, bottom=[r + n + w for r, n, w in zip(rent_expenses, needs_expenses_costs, wants_expenses_costs)], label='Remaining Income', color='gold', edgecolor="black", alpha=0.7)
        plt.title("Expense Analysis: Renting Scenario")
        plt.xlabel("Year")
        plt.ylabel(f"Cost ({currency})")
        # Setting the formatter for y-axis
        plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))
        plt.legend()
        plt.savefig(RENTING_GRAPH_PATH)
        plt.close()


        # Plotting Homeownership Scenario
        plt.figure(figsize=(10, 6))
        plt.bar(years_range, mortgage_payment, label='Mortgage', color='steelblue', edgecolor="black", alpha=0.7)
        plt.bar(years_range, needs_expenses_costs, bottom=mortgage_payment, label='Needs', color='lightgreen', edgecolor="black", alpha=0.7)
        plt.bar(years_range, wants_expenses_costs, bottom=[m + n for m, n in zip(mortgage_payment, needs_expenses_costs)], label='Wants', color='lightcoral', edgecolor="black", alpha=0.7)
        plt.bar(years_range, remaining_income_mortgage, bottom=[m + n + w for m, n, w in zip(mortgage_payment, needs_expenses_costs, wants_expenses_costs)], label='Remaining Income', color='gold', edgecolor="black", alpha=0.7)
        plt.title("Expense Analysis: Homeownership Scenario")
        plt.xlabel("Year")
        plt.ylabel(f"Cost ({currency})")
        # Setting the formatter for y-axis
        plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))
        plt.legend()
        plt.savefig(OWNERSHIP_GRAPH_PATH)
        plt.close

        logging.info("Expense analysis graphs generated successfully!")


        # Plotting Non-Recoverable Cost Graph
        homeownership_costs = data["non_recoverable_costs"][0]["homeownership_costs"]
        renting_costs = data["non_recoverable_costs"][0]["renting_costs"]

        plt.figure(figsize=(10, 6))
        plt.plot(years_range, homeownership_costs, label='Homeownership Costs', marker='o')
        plt.plot(years_range, renting_costs, label='Renting Costs', marker='o')
        plt.fill_between(years_range, homeownership_costs, renting_costs, color='gray', alpha=0.2)
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.title("Yearly Non-Recoverable Costs: Homeownership vs Renting")
        plt.xlabel("Year")
        plt.ylabel(f"Cost ({currency})")
        # Setting the formatter for y-axis
        plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(NON_RECOVERABLE_COSTS_GRAPH_PATH)
        plt.close()

        logging.info("Non-recoverable costs graph generated successfully!")

        # Plotting Opportunity Cost Graph
        # print(data["opportunity_costs"][0])
        home_equity_growth = data["opportunity_costs"][0]["home_equity_growth"]
        stock_investment_growth = data["opportunity_costs"][0]["stock_investment_growth"]

        plt.figure(figsize=(10, 6))
        plt.plot(years_range, home_equity_growth, label='Home Equity Growth', marker='o')
        plt.plot(years_range, stock_investment_growth, label='Stock Market Growth', marker='o')
        plt.fill_between(years_range, home_equity_growth, stock_investment_growth, color='gray', alpha=0.2)
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.title("Yearly Opportunity Costs: Homeownership vs Stock Market Investing")
        plt.xlabel("Year")
        plt.ylabel(f"Value ({currency})")
        # Setting the formatter for y-axis
        plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(OPPORTUNITY_COST_GRAPH_PATH)
        plt.close()

        logging.info("Opportunity Costs graph generated successfully!")

        # Generate Report        
        report_filename = generate_pdf_report(data)

        return report_filename

    except Exception as e:
        print(f"Error in generating report: {e}")
        logging.error(f"Output error: {e}")
        raise



def generate_pdf_report(data):
    """Creates a well structured PDF Report."""

    try:
        print(data)
        # Report Name
        name = data["user_details"][0]["name"]
        last_name = name.split()[-1]
        report_date = datetime.now().strftime("%Y-%m-%d")
        report_count = len(os.listdir(REPORTS_FOLDER))  # Count the number of reports generated
        report_filename = f"{REPORTS_FOLDER}/{last_name}_{report_date}_Report{report_count + 1}.pdf"
        monthly_mortgage_payment = data["user_details"][2]["monthly_mortgage_payment"] / 12
        currency = data["user_details"][0]["currency"]

        # Create PDF report
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Cover Page
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=20)
        pdf.ln(20)
        pdf.cell(200, 10, txt="Home Buying Analysis Report", ln=True, align='C')
        pdf.ln(20)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Prepared for: {name}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True, align='C')
        pdf.ln(20)

        # Table of Contents
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, "Table of Contents", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        cell_height = pdf.font_size * 1.5

        toc_items = TOC
        for item in toc_items:
            pdf.cell(0, cell_height, item, ln=True)
        pdf.ln(10)


        # Executive Summary
        pdf.add_page()
        cell_height = pdf.font_size * 1.3

        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Executive Summary", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, cell_height, EXECUTIVE_SUMMARY)

        pdf.ln(30)
        # Methodology
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Methodology", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, cell_height, METHODOLOGY)

        # Report Title
        pdf.add_page()
        pdf.ln(20)
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Home Buying Analysis Report", ln=True, align='C')
        pdf.ln(20)

        cell_width = 75
        cell_height = pdf.font_size * 1.3

        # Client details
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(180, 10, "Client Details", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(cell_width, cell_height, "Client Name: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][0]['name']}", ln=True)
        pdf.cell(cell_width, cell_height, "Age: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][0]['age']}", ln=True)
        pdf.cell(cell_width, cell_height, "Occupation: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][0]['occupation']}", ln=True)
        pdf.cell(cell_width, cell_height, "Marital Status: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][0]['status']}", ln=True)
        pdf.cell(cell_width, cell_height, "Country of Residence: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][0]['residence']}", ln=True)
        pdf.ln(10)

        # Financial details
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(180, 10, "Financial Details", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(cell_width, cell_height, "Annual Income: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{currency} {data['user_details'][1]['annual_income']:,.2f}", ln=True)
        pdf.cell(cell_width, cell_height, "Monthly Income: ", 0)
        pdf.cell(cell_width, cell_height, txt=f"{currency} {data['user_details'][1]['monthly_income']:,.2f}", ln=True)
        pdf.ln(10)


        # Property details
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(180, 10, "Property Details", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(cell_width, cell_height, "Property Value: ")
        pdf.cell(cell_width, cell_height, txt=f"{currency} {data['user_details'][2]['property_value']:,.2f}", ln=True)
        pdf.cell(cell_width, cell_height, "Deposit: ")
        pdf.cell(cell_width, cell_height, txt=f"{currency} {data['user_details'][2]['deposit']:,.2f}", ln=True)
        pdf.cell(cell_width, cell_height, "Monthly Mortgage Payment:")
        pdf.cell(cell_width, cell_height, txt=f"{currency} {monthly_mortgage_payment:,.2f}", ln=True)
        pdf.cell(cell_width, cell_height, "Mortgage Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][2]['mortgage_rate']}%", ln=True)
        pdf.ln(10)


        # Rates
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(180, 10, txt="Rates", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(cell_width, cell_height, "Rent Inflation Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][3]['rent_inflation']}%", ln=True)
        pdf.cell(cell_width, cell_height, "Income Growth Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][3]['income_growth']}%", ln=True)
        pdf.cell(cell_width, cell_height, "Property Growth Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][3]['property_growth']}%", ln=True)            
        pdf.cell(cell_width, cell_height, "Property Tax Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][3]['property_tax_rate']}%", ln=True)
        pdf.cell(cell_width, cell_height, "Annual Maintenance Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][3]['maintenance_rate']}%", ln=True)
        pdf.cell(cell_width, cell_height, "Stock Growth Rate: ")
        pdf.cell(cell_width, cell_height, txt=f"{data['user_details'][3]['stock_growth_rate']}%", ln=True)
        pdf.ln(10)

        # Expense Analysis
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Expense Analysis", ln=True)
        pdf.ln(5)

        # Stacked Bar Charts
        # Expense Analysis: Renting Scenario Stacked Bar Chart
        pdf.ln(5)
        pdf.image(RENTING_GRAPH_PATH, x=10, y=None, w=180)

        years = len(data["expense_cost_analysis"][0]["mortgage"])
        rent_expenses = data["expense_cost_analysis"][0]["rent_expenses"]
        remaining_income_rent = data["expense_cost_analysis"][0]["remaining_income_rent"]
        remaining_income_rent_pv = data["expense_cost_analysis"][0]["remaining_income_rent_pv"]
        remaining_income_mortgage = data["expense_cost_analysis"][0]["remaining_income_mortgage"]
        remaining_income_mortgage_pv = data["expense_cost_analysis"][0]["remaining_income_mortgage_pv"]

        # Expense Analysis: Homeownership Scenario Stacked Bar Chart
        pdf.image(OWNERSHIP_GRAPH_PATH, x=10, y=None, w=180)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 6, txt=f"Accummulated Remaining Income After Rent (Present Value): {currency} {remaining_income_rent_pv:,.2f}", ln=True)
        pdf.cell(200, 6, txt=f"Accummulated Remaining Income After Mortgage (Present Value): {currency} {remaining_income_mortgage_pv:,.2f}", ln=True)
        pdf.ln(5)

        remaining_income_difference = remaining_income_rent_pv - remaining_income_mortgage_pv
        remaining_title = ""

        if remaining_income_difference > 0:
            remaining_title = "Renting"
        elif remaining_income_difference < 0:
            remaining_title = "Buying a house"
        else:
            remaining_title = "Equal"

        expense_summary = f"""{remaining_title} is more cost effective with present value difference of {currency} {abs(remaining_income_difference):,.2f}."""
        pdf.cell(200, 8, expense_summary, ln=True)
        pdf.ln(10)

        # Table headers
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=12)
        col_width = 210 / 4.5
        row_height = pdf.font_size * 1.3
        pdf.cell(col_width * 0.6, row_height, "Year", 1, align="C")
        pdf.cell(col_width * 1.1, row_height, f"Rent Cost \n({currency})", 1, align="C")
        pdf.cell(col_width * 1.1, row_height, f"Income - Rent ({currency})", 1, align="C")
        # pdf.cell(40, 8, "Mortgage Cost (£)", 1, align="C")
        pdf.cell(col_width * 1.1, row_height, f"Income - Morgage ({currency})", 1, align="C", ln=True)

        # Add yearly values to table
        pdf.set_font("Arial", size=12)
        col_width = 210 / 4.5
        row_height = pdf.font_size * 1.3
        for year in range(years):
            pdf.cell(col_width * 0.6, row_height, str(year + 1), 1, align="C")
            pdf.cell(col_width * 1.1, row_height, f"{rent_expenses[year]:,.2f}", 1, align="R")
            pdf.cell(col_width * 1.1, row_height, f"{remaining_income_rent[year]:,.2f}", 1, align="R")
            # pdf.cell(40, 8, f"£ {mortgage_expenses[year]:,.2f}", 1, align="R")
            pdf.cell(col_width * 1.1, row_height, f"{remaining_income_mortgage[year]:,.2f}", 1, align="R", ln=True)


        # Non-Recoverable Costs
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Non-Recoverable Costs Analysis", ln=True)
        pdf.ln(5)

        homeownership_costs = data["non_recoverable_costs"][0]["homeownership_costs"]
        renting_costs = data["non_recoverable_costs"][0]["renting_costs"]
        nonrecoverable_cost_difference = data["non_recoverable_costs"][0]["nonrecoverable_cost_difference"]
        homeownership_costs_pv = data["non_recoverable_costs"][0]["homeownership_costs_pv"]
        renting_costs_pv = data["non_recoverable_costs"][0]["renting_costs_pv"]

        # Line Graph
        # Yearly Non-Recoverable Costs: Homeownership vs Renting
        pdf.ln(5)
        pdf.image(NON_RECOVERABLE_COSTS_GRAPH_PATH, x=10, y=None, w=180)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 6, txt=f"Accummulated Non-Recoverable Cost - Rent (Present Value): {currency} {renting_costs_pv:,.2f}", ln=True)
        pdf.cell(200, 6, txt=f"Accummulated Non-Recoverable Cost - Mortgage (Present Value): {currency} {homeownership_costs_pv:,.2f}", ln=True)

        nrc_difference_pv = homeownership_costs_pv - renting_costs_pv
        remaining_title_1 = ""
        if nrc_difference_pv > 0:
            remaining_title_1 = "Renting"
        elif nrc_difference_pv < 0:
            remaining_title_1 = "Buying a house"
        else:
            remaining_title_1 = "Equal"

        non_recoverable_summary = f"""{remaining_title_1} is more cost effective with present value difference (cheaper) of {currency} {abs(nrc_difference_pv):,.2f}."""
        pdf.cell(200, 8, non_recoverable_summary, ln=True)
        pdf.ln(10)


        # Table headers
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=12)
        col_width = 210 / 3.3
        row_height = pdf.font_size * 1.3
        pdf.cell(col_width * 0.7, row_height, "Year", 1, align="C")
        pdf.cell(col_width * 1.1, row_height, f"Homeownership \nCost ({currency})", 1, align="C")
        pdf.cell(col_width * 1.1, row_height, f"Rent Cost \n({currency})", 1, align="C", ln=True)

        # # Add yearly values to table
        pdf.set_font("Arial", size=12)
        col_width = 210 / 3.3
        row_height = pdf.font_size * 1.3
        for year in range(years):
            pdf.cell(col_width * 0.7, row_height, str(year + 1), 1, align="C")
            pdf.cell(col_width * 1.1, row_height, f"{homeownership_costs[year]:,.2f}", 1, align="R")
            pdf.cell(col_width * 1.1, row_height, f"{renting_costs[year]:,.2f}", 1, ln=True, align="R")
       

        # Opportunity Cost
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 8, txt="Opportunity Cost Analysis", ln=True)
        pdf.ln(5)

        home_equity_growth = data["opportunity_costs"][0]["home_equity_growth"]
        stock_investment_growth = data["opportunity_costs"][0]["stock_investment_growth"]
        opportunity_cost_difference = data["opportunity_costs"][0]["opportunity_cost_difference"]
        home_equity_pv = data["opportunity_costs"][0]["home_equity_pv"]
        stock_investment_pv = data["opportunity_costs"][0]["stock_investment_pv"]

        # Yearly Opportunity Costs: Homeownership vs Stock Market Investing
        pdf.ln(5)
        pdf.image(OPPORTUNITY_COST_GRAPH_PATH, x=10, y=None, w=180)

        oc_difference_pv = home_equity_pv - stock_investment_pv
        remaining_title_2 = ""
        if oc_difference_pv > 0:
            remaining_title_2 = "Buying a house"
        elif oc_difference_pv < 0:
            remaining_title_2 = "Renting and Investing"
        else:
            remaining_title_2 = "Equal"

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 6, txt=f"Accummulated Home Equity (Present Value): {currency} {home_equity_pv:,.2f}", ln=True)
        pdf.cell(200, 6, txt=f"Accummulated Stock Investment (Present Value): {currency} {stock_investment_pv:,.2f}", ln=True)
        opportunity_cost_summary = f"""{remaining_title_2} is will provide higher valuation present value difference of {currency} {abs(oc_difference_pv):,.2f}."""
        pdf.cell(200, 8, opportunity_cost_summary, ln=True)


        pdf.ln(10)


        # Table headers
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=12)
        col_width = 210 / 3.3
        row_height = pdf.font_size * 1.3
        pdf.cell(col_width * 0.8, row_height, "Year", 1, align="C")
        pdf.cell(col_width, row_height, f"Home Equity ({currency})", 1, align="C")
        pdf.cell(col_width, row_height, f"Stock Investment ({currency})", 1, align="C", ln=True)

        # Calculate yearly equity and investment values
        pdf.set_font("Arial", size=12)
        col_width = 210 / 3.3
        row_height = pdf.font_size * 1.3
        for year in range(years):
            pdf.cell(col_width * 0.8, row_height, str(year + 1), 1, align="C")
            pdf.cell(col_width, row_height, f"{home_equity_growth[year]:,.2f}", 1, align="R")
            pdf.cell(col_width, row_height, f"{stock_investment_growth[year]:,.2f}", 1, align="R", ln=True)


        # Add Conclusion
        pdf.add_page()

        # Bar Differential Graph
        conclusion_data = {
            "Expense Analysis (Spending Space)": (remaining_income_rent_pv, remaining_income_mortgage_pv),
            "Non-Recoverable Cost Analysis (Expense)": (renting_costs_pv, homeownership_costs_pv),
            "Opportunity Cost": (stock_investment_pv, home_equity_pv)
        }
        conclusion_graph = generate_conclusion_graphs(data, conclusion_data)

        conclusion = generate_conclusion(data)


        pdf.ln(10)
        col_width = 85
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Conclusion", ln=True, align='L')
        pdf.ln(5)
        pdf.set_font("Arial", size=12)

        pdf.cell(200, row_height, "Expense Analysis", align="L", ln=True)
        pdf.cell(col_width, row_height, "Acc. Remaining Income - Rent", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {remaining_income_rent_pv:,.2f}", 1, align="L", ln=True)
        pdf.cell(col_width, row_height, "Acc. Remaining Income - Homeownership", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {remaining_income_mortgage_pv:,.2f}", 1, align="L", ln=True)
        pdf.cell(col_width, row_height, "Difference", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {remaining_income_difference:,.2f}", 1, align="L", ln=True)
        pdf.ln(5)

        pdf.cell(200, row_height, "Non-Recoverable Cost Analysis", align="L", ln=True)
        pdf.cell(col_width, row_height, "Non-Recoverable Cost - Rent", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {renting_costs_pv:,.2f}", 1, align="L", ln=True)
        pdf.cell(col_width, row_height, "Non-Recoverable Cost - Homeownership", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {homeownership_costs_pv:,.2f}", 1, align="L", ln=True)
        pdf.cell(col_width, row_height, "Difference", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {nrc_difference_pv:,.2f}", 1, align="L", ln=True)
        pdf.ln(5)

        pdf.cell(200, row_height, "Opportunity Cost", align="L", ln=True)
        pdf.cell(col_width, row_height, "Accummulated Stock Investment", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {stock_investment_pv:,.2f}", 1, align="L", ln=True)
        pdf.cell(col_width, row_height, "Accummulated Home Equity", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {home_equity_pv:,.2f}", 1, align="L", ln=True)
        pdf.cell(col_width, row_height, "Difference", 1, align="L")
        pdf.cell(col_width, row_height, f"{currency} {oc_difference_pv:,.2f}", 1, align="L", ln=True)
        pdf.ln(15)

        pdf.image(conclusion_graph, x=10, y=None, w=180)

        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, row_height, conclusion)

        # Disclaimer
        pdf.ln(30)
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Disclaimer", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, row_height, DISCLAIMER)

        # Save and open the PDF
        pdf.output(report_filename)
        # sg.popup(f"Report generated: {report_filename}")
        os.system(f"start {report_filename}" if os.name == "nt" else f"open {report_filename}")

        logging.info(f"Report generated: {report_filename}")

        # Open the generated report automatically
        os.system(f"open {report_filename}" if os.name == "posix" else f"start {report_filename}")

        return report_filename


    except Exception as e:
        print(f"Error generating a report file: {e}")
        logging.error(f"Output Error: {e}")

    pass


def generate_conclusion(data):
    """
    Generate a detailed conclusion with analysis of non-recoverable costs and opportunity costs.
    """
    currency = data["user_details"][0]["currency"]

    conclusion = []

    # Expense Analysis
    remaining_income_mortgage = data["expense_cost_analysis"][0]["remaining_income_mortgage"]
    remaining_income_mortgage_pv = data["expense_cost_analysis"][0]["remaining_income_mortgage_pv"]
    remaining_income_rent_pv = data["expense_cost_analysis"][0]["remaining_income_rent_pv"]
    remaining_income_difference = remaining_income_rent_pv - remaining_income_mortgage_pv
    conclusion.append("Expense Analysis:")
    if remaining_income_difference > 0:
        conclusion.append(f"Renting provides better spending space with accummulated present value spending space difference of {currency} {abs(remaining_income_difference):,.2f}.")
    else:
        conclusion.append(f"Homeownership provides better spending space with accummulated present value spending space difference of {currency} {abs(remaining_income_difference):,.2f}.")

    # Non-Recoverable Cost Analysis
    homeownership_costs = data["non_recoverable_costs"][0]["homeownership_costs"]
    renting_costs = data["non_recoverable_costs"][0]["renting_costs"]
    nonrecoverable_cost_difference = data["non_recoverable_costs"][0]["nonrecoverable_cost_difference"]

    conclusion.append("\n\nNon-Recoverable Costs:")
    if nonrecoverable_cost_difference > 0:
        conclusion.append(f"Renting is more cost-effective over the analysis period, with a present value savings of {currency} {abs(nonrecoverable_cost_difference):,.2f}.")
    else:
        conclusion.append(f"Homeownership is more cost-effective over the analysis period, with a present value savings of {currency} {abs(nonrecoverable_cost_difference):,.2f}.")

    # Opportunity Cost Analysis
    home_equity_growth = data["opportunity_costs"][0]["home_equity_growth"]
    stock_investment_growth = data["opportunity_costs"][0]["stock_investment_growth"]
    opportunity_cost_difference = data["opportunity_costs"][0]["opportunity_cost_difference"]

    conclusion.append("\n\nOpportunity Costs:")
    if opportunity_cost_difference < 0:
        conclusion.append(f"Investing in the stock market offers better financial growth, with a present value advantage of {currency} {abs(opportunity_cost_difference):,.2f}.")
    else:
        conclusion.append(f"Homeownership equity growth outperforms stock investments, with a present value advantage of {currency} {abs(opportunity_cost_difference):,.2f}.")

    # Final Recommendation
    conclusion.append("\n\n\nRecommendation:")
    # if non_recoverable_pv > 0 and opportunity_cost_pv > 0:
    #     conclusion.append("Based on the analysis, homeownership is the preferable financial choice.")
    # elif non_recoverable_pv < 0 and opportunity_cost_pv < 0:
    #     conclusion.append("Renting and investing in the stock market is the better financial choice.")
    # else:
    #     conclusion.append("The choice depends on your risk appetite and preference for equity growth versus liquidity.")

    return "\n".join(conclusion)


def generate_conclusion_graphs(data, conclusion_data):
    # print(conclusion_data)
    currency = data["user_details"][0]["currency"]

    group = ["Rent", "Homeownership"]
    data = conclusion_data

    x = np.arange(len(group)) # the label locations
    width = 0.25 # width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")

    for factor, measurement in data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=factor)
        # Applying the comma_formatter to bar labels
        ax.bar_label(rects, padding=3, labels=[comma_formatter(i, 0) for i in measurement])
        # ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title, and custom x-axis tick labels, etc.
    ax.set_ylabel(f"Value ({currency})")
    ax.set_title("Renting vs Homeownership")
    ax.set_xticks(x + width, group)
    # Setting the formatter for y-axis
    ax.yaxis.set_major_formatter(FuncFormatter(comma_formatter))
    # Adjust the legend
    ax.legend(
        loc='upper center',         # Position: 'upper left', 'upper right', 'lower left', 'lower right', etc.
        fontsize='small',           # Font size: 'small', 'medium', 'large', or a float
        title=None,                 # Legend title
        ncol=2,                     # Number of columns
        frameon=True,               # Whether to draw a frame around the legend
        fancybox=True,              # Fancy frame (rounded corners)
        shadow=True,                 # Shadow effect
        # bbox_to_anchor=(0.5, 1.15) # Adjust position using a bounding box
    )
    # ax.legend(loc="upper left", ncols=2, fontsize="small", shadow=True, fancybox=True)
    max_value = max([max(measurement) for measurement in data.values()])
    ax.set_ylim(0, max_value * 1.2)

    plt.savefig(SUMMARY_GRAPH)
    plt.close()

    logging.info("Summary graph generated successfully!")

    return SUMMARY_GRAPH


# Function to format the tick labels with commas
def comma_formatter(x, pos):
    return '{:,}'.format(int(x))