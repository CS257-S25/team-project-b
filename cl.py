"""Command line interface for the covid_stats module"""
import sys
from ProductionCode import covid_stats

def print_usage():
    """Prints usage instructions for the command line"""
    print("""Usage:
    python cl.py compare country1,country2,... date
    python cl.py stats country beginning_date ending_date
    """)

def handle_compare(countries_arg, week):
    """Handles the compare command between 2–5 countries"""
    countries = countries_arg.split(",")
    if not 2 <= len(countries) <= 5:
        print("You must select between 2 and 5 countries.\n")
        print_usage()
        return
    text_output, _ = covid_stats.compare(countries, week)
    print(text_output)

def handle_stats(country, beginning_date, ending_date):
    """Handles the stats command for one country"""
    cases, deaths, actual_start, actual_end =covid_stats.get_cases_and_deaths_stats(country,
                                            beginning_date, ending_date)
    if cases is None or deaths is None:
        print(f"No data found for {country} in the given date range.")
    else:
        print(f"""Total cases in {country} from {actual_start} to {actual_end}: {cases}
    Total deaths in {country} from {actual_start} to {actual_end}: {deaths}""")

def command(args):
    """Dispatches based on command line args"""
    if len(args) == 0:
        print_usage()
        return

    command_arg = args[0]
    if command_arg == "compare" and len(args) == 3:
        handle_compare(args[1], args[2])
    elif command_arg == "stats" and len(args) == 4:
        handle_stats(args[1], args[2], args[3])
    else:
        print("Invalid command or wrong number of arguments.\n")
        print_usage()

def main():
    """Entry point for CLI"""
    args = sys.argv[1:]
    command(args)

if __name__ == "__main__":
    main()
