import json
import logging
import numpy as np
import os
import pandas as pd
import requests

from datetime import datetime

CURRENT_DIR = os.getcwd()
OUTPUT_FOLDER = "Country Data"

# List of countries (ISO Alpha-2 codes)
COUNTRIES = [
    "US", "GB", "DE", "FR", "JP", "CA", "AU", "KR", "SG", "NZ", "CN", "IN", "BR", "MX", "RU",
    "ZA", "TR", "ID", "SA", "AE", "QA", "TH", "PH"
]

# World Bank economic indicators
INDICATORS = {
    "GDP (USD)": "NY.GDP.MKTP.CD",  # GDP in current US dollars
    "Inflation, consumer prices (%)": "FP.CPI.TOTL.ZG",  # Inflation (CPI, annual %)
    "Interest Rate (%)": "FR.INR.RINR"   # Real interest rate (%)
}

def generate_country_directory():

    # os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    # countries_finance = "countries_finance_data.txt" 
    # file_path = f"{CURRENT_DIR}/{OUTPUT_FOLDER}/{countries_finance}"
    

    # Set the date range
    start_date = datetime(1974, 1, 1)
    end_date = datetime(2023, 1, 1)


    # Convert DataFrame to dictionary
    finance_data = {}
    for country in COUNTRIES:
        country_data = {}
        for name, code in INDICATORS.items():
            value = get_world_bank_data(country, code)
            country_data[name] = value
        finance_data[country] = country_data

    
    # if not os.path.exists(file_path):
    #     with open(file_path, "w") as file:
    #         file.write(str(finance_data))

    return finance_data


def get_world_bank_data(country, indicator):
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1 and data[1]:
            return data[1][0].get("value", None)
    return None
