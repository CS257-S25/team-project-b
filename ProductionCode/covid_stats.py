"""This module provides functions to calculate COVID-19 statistics
for given countries and date ranges using the DataSource class."""

from .datasource import DataSource

# Create one shared database connection
ds = DataSource()

def stats(country, beginning_date, ending_date):
    """Calculates total cases and deaths for a country in a date range."""
    try:
        cursor = ds.connection.cursor()
        query = """
            SELECT SUM(New_cases), SUM(New_deaths)
            FROM bigTable
            WHERE Country = %s AND Date_reported BETWEEN %s AND %s;
        """
        cursor.execute(query, (country, beginning_date, ending_date))
        result = cursor.fetchone()
        cursor.close()

        total_cases = result[0] if result[0] else 0
        total_deaths = result[1] if result[1] else 0

        return total_cases, total_deaths

    except Exception as e:
        print("Error in stats():", e)
        return 0, 0

def compare(countries, week):
    """Compares stats for multiple countries on one date."""
    output = ""
    for country in countries:
        cases, deaths = stats(country, week, week)
        output += (f"""Total cases in {country} during {week}: {cases}\n
Total deaths in {country} during {week}: {deaths}\n\n""")
    return output

if __name__ == "__main__":
    print(compare(["Afghanistan", "Brazil"], "2023-08-06"))
    ds.connection.close()
