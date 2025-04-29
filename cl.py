import sys
from ProductionCode import covid_stats


def print_usage():
    print("""Usage:\n
          python cl.py compare country1,country2 beginning_date ending_date\n
          python cl.py stats country beginning_date ending_date
          """)

    
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
        week = args[2]
        covid_stats.compare(countries, week)

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