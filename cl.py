import sys
from ProductionCode import covid_stats


def print_usage():
    print("Usage:")
    print("  python cl.py compare country1,country2..country5 date")
    print("  python cl.py stats country beginning_date ending_date")
    print("  python cl.py highest beginning_date ending_date")

def handle_compare(countries_arg, week):
    countries = countries_arg.split(",")
    if not (2 <= len(countries) <= 5):
        print_usage()
        return
    covid_stats.compare(countries, week)

def handle_stats(country, beginning_date, ending_date):
    cases, deaths = covid_stats.stats(country, beginning_date, ending_date)
    print(f"Total cases in {country} from {beginning_date} to {ending_date}: {cases}")
    print(f"Total deaths in {country} from {beginning_date} to {ending_date}: {deaths}")

def command(args):
    if len(args) == 0:
        print_usage()
        return

    command = args[0]

    if command == "compare" and len(args) == 3:
        handle_compare(args[1], args[2])
    elif command == "stats" and len(args) == 4:
        handle_stats(args[1], args[2], args[3])
    elif command == "highest" and len(args) == 3:
        handle_highest(args[1], args[2])
    else:
        print_usage()

def main():
    args = sys.argv[1:]
    process_command(args)

if __name__ == "__main__":
    main()
