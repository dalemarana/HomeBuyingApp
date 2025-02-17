# import json
# import logging
# import numpy as np
import os
# import pandas as pd
import requests

from datetime import datetime
from home_buying_app.config import EXCHANGE_RATE_API_KEY

"""
This code uses the following APIs:
    - World Bank API to get the following data
        - Economic data (GDP, Inflation, and Interest Rate)
        - General Country data (Name, Region, Income Level, Capital City)
    - REST Countries API
        - Currency
    - Exchange Rate API
        - Exchange Rate to USD
"""

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
    financial_data = {}
    for country in COUNTRIES:
        country_data = {}
        # Get economic indicators
        for name, code in INDICATORS.items():
            value = get_world_bank_data(country, code)
            country_data[name] = value
        # Get country information
        country_info = get_country_data(country)
        country_data.update(country_info)
        # Get currency code dynamically
        currency_code = get_currency_code(country)
        country_data["currency"] = currency_code
        # Get exchange rate to USD
        if currency_code:
            exchange_rate = get_exchange_rate(currency_code)
            country_data["exchange_rate_to_usd"] = exchange_rate
        else:
            country_data["exchange_rate_to_usd"] = None
        
        financial_data[country] = country_data

    
    # if not os.path.exists(file_path):
    #     with open(file_path, "w") as file:
    #         file.write(str(finance_data))

    return financial_data


# Function to get country financial information from World Bank API
def get_world_bank_data(country, indicator):
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1 and data[1]:
            return data[1][0].get("value", None)
    return None


# Function to get country information
def get_country_data(country):
    url = f"http://api.worldbank.org/v2/country/{country}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1 and data[1]:
            return {
                "name": data[1][0].get("name", None),
                "region": data[1][0].get("region", {}).get("value", None),
                "incomeLevel": data[1][0].get("incomeLevel", {}).get("value", None),
                "capitalCity": data[1][0].get("capitalCity", None),
            }
    return {}


# Function to get currency code dynamically
def get_currency_code(country):
    url = f"https://restcountries.com/v3.1/alpha/{country}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        currencies = data[0].get("currencies", {})
        if currencies:
            return list(currencies.keys())[0]  # Return the first currency code
    return None


# Function to get exchange rate to USD
def get_exchange_rate(currency_code):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data.get("conversion_rates", {})
        return rates.get(currency_code, None)
    return None