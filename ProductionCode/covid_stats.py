"""This module provides functions to calculate COVID-19 statistics
for given countries and date ranges."""
import csv
from datetime import datetime

# Load data once
with open('Data/WHO-COVID-19-global-data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = list(reader)

def stats(country, beginning_date, ending_date):
    """Calculates the total number of cases and deaths for a given country
    between two dates.
    Args:
        country (str): The name or code of the country.
        beginning_date (str): The start date in "YYYY-MM-DD" format.
        ending_date (str): The end date in "YYYY-MM-DD" format.
   """
    beginning = datetime.strptime(beginning_date, "%Y-%m-%d")
    ending = datetime.strptime(ending_date, "%Y-%m-%d")

    total_cases = 0
    total_deaths = 0

    for row in data:  # use already loaded data
        if country in (row['Country'], row['Country_code']):
            date = datetime.strptime(row['Date_reported'], "%Y-%m-%d")

            if beginning <= date <= ending:
                if row['New_cases'] != '':
                    total_cases += int(row['New_cases'])
                if row['New_deaths'] != '':
                    total_deaths += int(row['New_deaths'])
    return total_cases, total_deaths

def compare(countries, week):
    """Compares the COVID-19 statistics for a list of countries
    for a given week.
    Args:
        countries (list): List of country names or codes.
        week (str): The week to compare statistics for.
    Returns:
        str: A formatted string with the comparison results.
    """
    output = ""
    results = []
    for country in countries:
        cases, deaths = stats(country, week, week)
        output += (f"""Total cases in {country} during {week}: {cases}\n
                   Total deaths in {country} from {week}: {deaths}\n""")
        results.append((country, cases, deaths))
    return output
