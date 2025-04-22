import sys
from ProductionCode import covid_stats

def print_usage():
    print("Usage:")
    print("  python cl.py compare country1,country2 beginning_date ending_date")
    print("  python cl.py stats country beginning_date ending_date")
    '''print("  python cl.py highest beginning_date ending_date")'''

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print_usage()
        return

    command = args[0]
    

    if command == "compare" and len(args) == 3:
        if not (2 <= len(args[1].split(",")) <= 5):
            print_usage()
            return
        countries = args[1].split(",")
        '''
        Country1 = countries[0]
        country2 = countries[1]
        country3 = countries[2] if len(countries) > 2 else None
        country4 = countries[3] if len(countries) > 3 else None
        country5 = countries[4] if len(countries) > 4 else None
        '''
        week = args[2]
        covid_stats.compare(countries, week)

    elif command == "stats" and len(args) == 4:
        country = args[1]
        beginning_date = args[2]
        ending_date = args[3]
        cases, deaths = covid_stats.stats(country, beginning_date, ending_date)
        print(f"Total cases in {country} from {beginning_date} to {ending_date}: {cases}")
        print(f"Total deaths in {country} from {beginning_date} to {ending_date}: {deaths}")

    elif command == "highest" and len(args) == 3:
        beginning_date = args[1]
        ending_date = args[2]
        covid_stats.highest(beginning_date, ending_date)

    else:
        print_usage()

if __name__ == "__main__":
    csv_reader = CSVReader()
    csv_reader.read_csv()
