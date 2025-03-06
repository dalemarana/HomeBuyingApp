import os
import logging
import datetime
import PySimpleGUI as sg

from ast import literal_eval
from home_buying_app.processing import process_data
from home_buying_app.output import generate_graphs_and_report
from home_buying_app.extras import country_data


DEFAULT_FOLDER = f"{os.getcwd()}/home_buying_app"
DATA_NEEDED = ["Inflation, consumer prices (%)", "Interest Rate (%)", "currency", "exchange_rate_to_usd"]

# Ensure required directories exist
REQUIRED_DIRECTORIES = ["User Input", "logs", "Instructions", "Country Data"]
for directory in REQUIRED_DIRECTORIES:
    os.makedirs(f"{DEFAULT_FOLDER}/folders/{directory}", exist_ok=True)

# Countries Data
COUNTRIES_DATA_PATH = f"{DEFAULT_FOLDER}/folders/Country Data/countries_finance_data.txt"
COUNTRY_DATA = {}
if not os.path.exists(COUNTRIES_DATA_PATH):
    with open(COUNTRIES_DATA_PATH, "w") as file:
        COUNTRY_DATA = country_data.generate_country_directory()
        file.write(str(COUNTRY_DATA))
else:
    with open(COUNTRIES_DATA_PATH, "r") as file:
        COUNTRY_DATA = literal_eval(file.read())


# Getting the List of countries
COUNTRY_INFLATION_INTEREST = {}
for key in COUNTRY_DATA:
    country_info = COUNTRY_DATA[key]
    country_data_list = []
    for _ in DATA_NEEDED:
        country_data_list.append(country_info[_])
    COUNTRY_INFLATION_INTEREST[country_info["name"]] = country_data_list

COUNTRY_NAMES = list(COUNTRY_INFLATION_INTEREST.keys())

# Default content for input files
DEFAULT_INPUTS = {
    f"{DEFAULT_FOLDER}/folders/User Input/client_details.txt": "name: John Doe\nage: 33\noccupation: Engineer\nstatus: Married\nresidence: United Kingdom",
    f"{DEFAULT_FOLDER}/folders/User Input/financial_details.txt": "annual_income: 90000\nmonthly_income: 5200",
    f"{DEFAULT_FOLDER}/folders/User Input/expenses.txt": "rent: 1475\nelectricity: 90\nwater: 25\ngroceries: 250\ncouncil_tax: 170\nother: 200",
    f"{DEFAULT_FOLDER}/folders/User Input/property_details.txt": "property_value: 440000\ndeposit: 44000\nduration: 33\nsolicitor: 3250\nsurvey: 750\nfurnishings: 3000"
}

# Create input files with default content if missing
for file_path, content in DEFAULT_INPUTS.items():
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(content)

# Create User Manual
USER_MANUAL = os.path.join("Instructions", "Home_Buying_Analysis_User_Manual.pdf")

# Configure logging
logging.basicConfig(
    filename=f"{DEFAULT_FOLDER}/folders/logs/home_buying.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class HomeBuyingAnalysis:
    def __init__(self):
        self.client_details = {}
        self.financial_details = {}
        self.expenses = {}
        self.property_details = {}
        self.interest_rate = 0.05
        self.custom_interest_rate = None


    # Reading Default Input files
    def read_input_files(self):
        try:
            self.client_details = self.read_file(f"{DEFAULT_FOLDER}/folders/User Input/client_details.txt")
            self.financial_details = self.read_file(f"{DEFAULT_FOLDER}/folders/User Input/financial_details.txt")
            self.expenses = self.read_file(f"{DEFAULT_FOLDER}/folders/User Input/expenses.txt")
            self.property_details = self.read_file(f"{DEFAULT_FOLDER}/folders/User Input/property_details.txt")

            logging.info("User input files loaded successfully.")
        except Exception as e:
            logging.error(f"Error reading input files: {e}")
            sg.popup_error("Error loading input files. Check the 'User Input' folder.")
            exit()

    # Function to add World Bank Data (Interest Rate and Inflation), Currency and Exchange Rate to Dictionary
    # def add_to_dict()

    @staticmethod
    def read_file(filepath):
        data = {}
        with open(filepath, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                data[key.strip()] = value.strip()
        return data


    def create_gui(self):
        """Creates and runs the GUI for user interaction."""

        sg.theme("DarkBlue")

        # Tab 1: Client Details
        tab1 = [
            [sg.Text("Name", size=(15,1)), sg.InputText(self.client_details.get("name", ""), key="name")],
            [sg.Text("Age", size=(15,1)), sg.InputText(self.client_details.get("age", ""), key="age")],
            [sg.Text("Occupation", size=(15,1)), sg.InputText(self.client_details.get("occupation", ""), key="occupation")],
            [sg.Text("Marital Status", size=(15,1)), sg.Combo(["Single", "Married"], default_value=self.client_details.get("status", ""), key="status")],
            [sg.Text("Current Residence", size=(15,1)), sg.Combo(COUNTRY_NAMES, default_value=self.client_details.get("residence", ""), key="residence")],
            # [sg.Text("Current Residence", size=(15,1)), sg.InputText(self.client_details.get("residence", ""), key="residence")],
        ]

        # Tab 2: Financial Details
        tab2 = [
            [sg.Text("Annual Gross Income", size=(20,1)), sg.InputText(self.financial_details.get("annual_income", ""), key="annual_income")],
            [sg.Text("Monthly Net Income", size=(20,1)), sg.InputText(self.financial_details.get("monthly_income", ""), key="monthly_income")],
        ]

        # Tab 3: Monthly Expenses
        tab3 = [
            [sg.Text("Rent", size=(15,1)), sg.InputText(self.expenses.get("rent", ""), key="rent")],
            [sg.Text("Electricity and Gas", size=(15,1)), sg.InputText(self.expenses.get("electricity", ""), key="electricity")],
            [sg.Text("Water", size=(15,1)), sg.InputText(self.expenses.get("water", ""), key="water")],
            [sg.Text("Groceries", size=(15,1)), sg.InputText(self.expenses.get("groceries", ""), key="groceries")],
            [sg.Text("Council Tax", size=(15,1)), sg.InputText(self.expenses.get("council_tax", ""), key="council_tax")],
            [sg.Text("Other Expenses", size=(15,1)), sg.InputText(self.expenses.get("other", ""), key="other")],
        ]

        # Tab 4: Property Details
        tab4 = [
            [sg.Text("Property Value", size=(15,1)), sg.InputText(self.property_details.get("property_value", ""), key="property_value")],
            [sg.Text("Deposit", size=(15,1)), sg.InputText(self.property_details.get("deposit", ""), key="deposit")],
            [sg.Text("Mortgage Term", size=(15,1)), sg.InputText(self.property_details.get("duration", ""), key="duration")],
            [sg.Text("Solicitor Fees", size=(15,1)), sg.InputText(self.property_details.get("solicitor", ""), key="solicitor")],
            [sg.Text("Survey Costs", size=(15,1)), sg.InputText(self.property_details.get("survey", ""), key="survey")],
            [sg.Text("Initial Furnishings", size=(15,1)), sg.InputText(self.property_details.get("furnishings", ""), key="furnishings")],
        ]

        # Tab 5: Interest Rates and Final Actions
        tab5 = [
            [sg.Text("Inflation (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="inflation", default_value=2.0)],
            [sg.Text("Interest Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="interest_rate", default_value=5.4)],
            [sg.Text("Rent Inflation Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="rent_inflation", default_value=4.0)],
            [sg.Text("Income Growth Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="income_growth", default_value=2.5)],
            [sg.Text("Property Growth Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="property_growth", default_value=4.0)],
            [sg.Text("Property Tax Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="property_tax_rate", default_value=0.0)],
            [sg.Text("Discount Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="discount_rate", default_value=3.0)],    
            [sg.Text("Annual Maintenance Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="maintenance_rate", default_value=1.0)],
            [sg.Text("Stock Growth Rate (%)", size=(25,1)), sg.Slider(range=(0.0, 10.0), resolution=0.1, orientation="h", key="stock_growth_rate", default_value=7.7)],
            [sg.Text(f"Reference Data as per World Bank Data (2023): ", size=(50,1))],
            [sg.Text(f"Consumer Price Index, Inflation:", size=(30,1)), sg.Text(key="Inflation, consumer prices (%)")],
            [sg.Text(f"Interest Rate: ", size=(30,1)), sg.Text(key="Interest Rate (%)")],
            [sg.Text(f"Currency: ", size=(30,1)), sg.Text(key="currency")],
            [sg.Text(f"Exchage rate to USD: ", size=(30,1)), sg.Text(key="exchange_rate_to_usd")],
            # [sg.Button("Show Graph", size=(20,1)), sg.Button("Generate Report"), sg.Button("Calculate Again")]
        ]

        tab6 = [
            [sg.Button("Generate Report", size=(20,1))],
            [sg.Button("Calculate Again", size=(20,1))],
            [sg.Button("Exit", size=(20,1))],
        ]

        # Layout with Tabs
        tab_group_layout = [[sg.Tab("Client Details", tab1, key="-TAB1-"),
            sg.Tab("Financial Details", tab2, visible=False, key="-TAB2-"),
            sg.Tab("Monthly Expenses", tab3, visible=False, key="-TAB3-"),
            sg.Tab("Property Details", tab4, visible=False, key="-TAB4-"),
            sg.Tab("Rates", tab5, visible=False, key="-TAB5-"),
            sg.Tab("Final Actions", tab6, visible=False, key="-TAB6-")]
        ]

        layout = [
            [sg.TabGroup(tab_group_layout, enable_events=True, key='TabGroup', selected_title_color='blue')],
            [sg.Button("Next", key="Next"), sg.Button("View User Manual", key="user_manual")]
        ]


        return sg.Window("Rent vs Buy Calculator", layout, finalize=True)

    

    def run_gui(self):

        self.window = self.create_gui()
        window = self.window

        current_tab = 1

        while True:
            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, "Exit"):
                if sg.popup_yes_no("Do you really want to exit?") == "Yes":
                    break

            # # Tab Navigation
            # if event.startswith("Next"):
            #     for i, key in enumerate(DATA_NEEDED):
            #         values[key] = COUNTRY_INFLATION_INTEREST[values.get("residence")][i]
            #         if key in ["Inflation, consumer prices (%)", "Interest Rate (%)"] and values[key] is not None:
            #             values[key] = round(values[key], 2)
            #         window[key].update(values[key])
            #     # print(f"GUI: {values}")
            #     current_tab += 1
            #     window[f"-TAB{current_tab}-"].update(visible=True).select()


            # Tab Navigation
            if event == "Next":
                for i, key in enumerate(DATA_NEEDED):
                    values[key] = COUNTRY_INFLATION_INTEREST.get(values.get("residence"), [None] * len(DATA_NEEDED))[i]
                    if key in ["Inflation, consumer prices (%)", "Interest Rate (%)"] and values[key] is not None:
                        values[key] = round(values[key], 2)
                    window[key].update(values[key])

                # tab_keys = ["-TAB1-", "-TAB2-", "-TAB3-", "-TAB4-", "-TAB5-"]
                # current_tab = window["TabGroup"].get()
                # print(current_tab)

                try:
                    if current_tab < 6:  # Prevent out-of-range errors
                        window[f"-TAB{current_tab}-"].update(visible=True)
                        window["TabGroup"].Widget.select(current_tab)  # ✅ Correct tab selection
                        current_tab += 1
                except IndexError:
                    print("Already on last tab!")  # No next tab available

                # if current_tab < 6:  # Prevent out-of-range errors
                #     window[f"-TAB{current_tab}-"].update(visible=True)
                #     window["TabGroup"].Widget.select(current_tab)  # ✅ Correct tab selection
                #     current_tab += 1


                    
            if event.startswith("Back"):
                current_tab -= 1
                window[f"Tab{current_tab}"].update(visible=True).select()

            # if event == "View User Manual":
            #     if os.path.exists(USER_MANUAL):
            #         print("Opening user manual...")
            #         os.startfile(USER_MANUAL)
            #     else:
            #         sg.popup_error("User Manual not found. Please contact support.")


            # Show Graph
            if event == "Show Graph":
                processed_data = process_data(values)

            # Generate Report
            if event == "Generate Report":
                for i, key in enumerate(DATA_NEEDED):
                    values[key] = COUNTRY_INFLATION_INTEREST[values.get("residence")][i]
                    if key in ["Inflation, consumer prices (%)", "Interest Rate (%)"] and values[key] is not None:
                        values[key] = round(values[key], 2)
                    window[key].update(values[key])
                processed_data = process_data(values)
                filename = generate_graphs_and_report(processed_data)
                sg.popup(f"Report generated: {filename}")


            # Reset Calculation
            if event == "Calculate Again":
                window.close()
                self.create_gui()

        self.window.close()

def run():
    app = HomeBuyingAnalysis()
    app.read_input_files()
    # app.create_gui()
    app.run_gui()