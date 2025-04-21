import csv

def stats (country, week):
    with open ('Data/WHO-COVID-19-global-data.csv', 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['Country'] == country and row['Date_reported'] == week:
                print(f"Country: {country}")
                print(f"Week: {week}")
                print(f"Cases: {row['New_cases']}")
                print(f"Deaths: {row['New_deaths']}")
                return            

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