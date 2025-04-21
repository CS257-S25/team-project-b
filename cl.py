import sys
from ProductionCode import covid_stats
def print_usage():
    print ("...")
def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print_usage()
        return

    command = args[0]
    if command == "compare" and len(args) == 3:
        countries = args[1].split(",")
        week = args[2]
        covid_stats.compare(countries, week)
    elif command == "stats" and len(args) == 3:
        country = args[1]
        week = args[2]
        covid_stats.stats(country, week)
    elif command == "highest" and len(args) == 2:
        week = args[1]
        covid_stats.highest(week)
    else :
        print_usage()
if __name__ == "__main__":
    main()

