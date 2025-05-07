import sys
from ProductionCode import covid_stats
"""Command line interface for the covid_stats module"""

def print_usage():
    """Prints usage instructions for the command line
    no arguments passed
    """
    print("""s""")

"""Usage:\n
          python cl.py compare country1,country2..country5 date\n
          python cl.py stats country beginning_date ending_date\n
          python cl.py highest beginning_date ending_date"""

def handle_compare(countries_arg, week):
    """Handles the compare command between 2+ countries
    Calls the compare function from covid_stats
    Passed arguments are:
    countries_arg
    week
    """
    countries = countries_arg.split(",")
    if not 2 <= len(countries) <= 5:
        print_usage()
        return
    covid_stats.compare(countries, week)

def handle_stats(country, beginning_date, ending_date):
    """Handles the stats command-calls for one country
    between two dates
    Calls the stats function from covid_stats
    Passed arguments are:
    country: str - first
    beginning_date: str - second
    ending_date: str - third
    """
    cases, deaths = covid_stats.stats(country, beginning_date, ending_date)
    print(f"""Total cases in {country} from {beginning_date} to {ending_date}: {cases}\n
          Total deaths in {country} from {beginning_date} to {ending_date}: {deaths}""")

def command(args):
    """Takes the command line arguments and calls the appropriate function
    based on the command
    compare or stats
    1 argument for either
    """
    if len(args) == 0:
        print_usage()
        return
    command_arg = args[0]
    if command_arg == "compare" and len(args) == 3:
        handle_compare(args[1], args[2])
    elif command_arg == "stats" and len(args) == 4:
        handle_stats(args[1], args[2], args[3])
    else:
        print_usage()

def main():
    """Main function to handle command line arguments"""
    args = sys.argv[1:]
    command(args)

if __name__ == "__main__":
    main()
