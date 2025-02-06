import logging
import numpy as np
import os
import pandas as pd
import wbdata

from datetime import datetime

def generate_country_directory():
    current_dir = os.getcwd()
    OUTPUT_FOLDER = "Country Data"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    countries_finance = "countries_finance_data.txt" 
    file_path = f"{current_dir}/{OUTPUT_FOLDER}/{countries_finance}"
    

    # Set the date range
    start_date = datetime(1974, 1, 1)
    end_date = datetime(2023, 1, 1)

    # List of countries (ISO Alpha-2 codes)
    countries = [
        "US", "GB", "DE", "FR", "JP", "CA", "AU", "KR", "SG", "NZ", "CN", "IN", "BR", "MX", "RU",
        "ZA", "TR", "ID", "SA", "AE", "QA", "TH", "PH"
    ]

    # World Bank economic indicators
    indicators = {
        "NY.GDP.MKTP.CD": "GDP (USD)",  # GDP in current US dollars
        "FP.CPI.TOTL.ZG": "Inflation Rate (%)",  # Inflation (CPI, annual %)
        "FR.INR.RINR": "Interest Rate (%)"  # Real interest rate (%)
    }

    # Fetch latest available data
    df = wbdata.get_dataframe(indicators, country=countries, parse_dates=False)#, convert_date=True)


    latest_year = f"{max(df.index)[1]}" # Get most recent year of data

    # Convert DataFrame to dictionary
    countries_finance_data = {}
    for country in countries:
        country_name = wbdata.get_countries(country)[0]["name"]
        countries_finance_data[country_name] = {
            "ISO Code": country,
            "Currency Code": None,  # World Bank API does not provide currency codes
            "GDP (USD)": float(df.loc[country_name, latest_year]["GDP (USD)"]),
            "Inflation Rate (%)": float(df.loc[country_name, latest_year]["Inflation Rate (%)"]),
            "Interest Rate (%)": float(df.loc[country_name, latest_year]["Interest Rate (%)"])
        }

    
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(str(countries_finance_data))

    logging.info("Country Data Generated.")

    print(countries_finance_data)
    print(f"United Kingdom: {countries_finance_data["United Kingdom"]}")



