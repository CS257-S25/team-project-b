import csv
from datetime import datetime

# Load data once
with open('Data/WHO-COVID-19-global-data.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

def stats(country, beginning_date, ending_date):
    beginning = datetime.strptime(beginning_date, "%Y-%m-%d")
    ending = datetime.strptime(ending_date, "%Y-%m-%d")

    total_cases = 0
    total_deaths = 0

    for row in data:  # use already loaded data
        if row['Country'] == country or row['Country_code'] == country:
            date = datetime.strptime(row['Date_reported'], "%Y-%m-%d")

            if beginning <= date <= ending:
                if row['New_cases'] != '':
                    total_cases += int(row['New_cases'])
                if row['New_deaths'] != '':
                    total_deaths += int(row['New_deaths'])
    return total_cases, total_deaths

def compare(countries, week):
    results = []
    for country in countries:
        cases, deaths = stats(country, week, week)
        print(f"""Total cases in {country} during {week}: {cases}!\n
              Total deaths in {country} from {week}: {deaths}\n""")
        results.append((country, cases, deaths))
    return results

'''
def highest(week):
    highest_cases = 0
    highest_country = ""
    for row in data:
        if row['Date_reported'] == week:
            if row['New_cases'] != '' and int(row['New_cases']) > highest_cases:
                highest_cases = int(row['New_cases'])
                highest_country = row['Country']
    print(f"Country with the highest cases in {week}: {highest_country} with {highest_cases} cases")
'''
