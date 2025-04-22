import csv
from datetime import datetime

def stats(country, beginning_date, ending_date):
    beginning = datetime.strptime(beginning_date, "%Y-%m-%d")
    ending = datetime.strptime(ending_date, "%Y-%m-%d")

    total_cases = 0
    total_deaths = 0

    with open('Data/WHO-COVID-19-global-data.csv', 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['Country'] == country:
                date = datetime.strptime(row['Date_reported'], "%Y-%m-%d")
                if beginning <= date <= ending:
                    total_cases += int(row['New_cases'])
                    total_deaths += int(row['New_deaths'])

    return total_cases, total_deaths

def highest (week):
    with open('Data/WHO-COVID-19-global-data.csv', 'r' ) as file:
        reader = csv.DictReader(file)
        highest_cases = 0
        highest_country = ""
        for row in reader:
            if row['Date_reported'] == week:
                if int(row['New_cases']) > highest_cases:
                    highest_cases = int(row['New_cases'])
                    highest_country = row['Country']
        print(f"Country with the highest cases in {week}: {highest_country} with {highest_cases} cases")