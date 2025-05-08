"""Command line interface for the covid_stats module"""
import sys
from ProductionCode import covid_stats

def print_usage():
    """Prints usage instructions for the command line"""
    print("""Usage:
    python cl.py compare country1,country2..country5 date
    python cl.py stats country beginning_date ending_date
    """)

def handle_compare(countries_arg, week):
    """Handles the compare command for multiple countries"""
    countries = countries_arg.split(",")
    if not 2 <= len(countries) <= 5:
        print("Please provide between 2 and 5 countries.")
        print_usage()
        return
    result = covid_stats.compare(countries, week)
    print(result)

def handle_stats(country, beginning_date, ending_date):
    """Handles the stats command for a single country"""
    cases, deaths = covid_stats.stats(country, beginning_date, ending_date)
    print(f"Total cases in {country} from {beginning_date} to {ending_date}: {cases}")
    print(f"Total deaths in {country} from {beginning_date} to {ending_date}: {deaths}")

def command(args):
    """Parses and routes CLI arguments to the appropriate function"""
    if len(args) == 0:
        print_usage()
        return
    command_arg = args[0]
    if command_arg == "compare" and len(args) == 3:
        handle_compare(args[1], args[2])
    elif command_arg == "stats" and len(args) == 4:
        handle_stats(args[1], args[2], args[3])
    else:
        print("Invalid arguments.")
        print_usage()

def main():
    args = sys.argv[1:]
    command(args)

if __name__ == "__main__":
    main()
