"""This module provides functions to calculate COVID-19 statistics
for given countries and date ranges using the DataSource class."""

from .datasource import DataSource

# Create one shared database connection
ds = DataSource()

def get_closest_date(target_date, country, before=True):
    """Get the closest available date for the country."""
    try:
        cursor = ds.connection.cursor()
        if before:
            query = """
                SELECT MAX(Date_reported) FROM bigTable
                WHERE Country = %s AND Date_reported <= %s;
            """
        else:
            query = """
                SELECT MIN(Date_reported) FROM bigTable
                WHERE Country = %s AND Date_reported >= %s;
            """
        cursor.execute(query, (country, target_date))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result and result[0] else None
    except Exception as e:
        print("Error finding closest date:", e)
        return None

def stats(country, beginning_date, ending_date):
    """Calculates total cases and deaths using closest available dates."""
    try:
        # Adjust dates to closest available
        start_date = DataSource.get_closest_date(beginning_date, country, before=False)
        end_date = DataSource.get_closest_date(ending_date, country, before=True)

        if not start_date or not end_date:
            return None, None, None, None  # No valid range

        """cursor = ds.connection.cursor()
        query = 
            SELECT SUM(New_cases), SUM(New_deaths)
            FROM bigTable
            WHERE Country = %s AND Date_reported BETWEEN %s AND %s;
        
        cursor.execute(query, (country, start_date, end_date))
        result = cursor.fetchone()
        cursor.close()"""



        result = DataSource.get_sum_between_dates(country, start_date)
        
        total_cases = result[0] or 0
        total_deaths = result[1] or 0

        return total_cases, total_deaths, start_date, end_date

    except Exception as e:
        print("Error in stats():", e)
        return None, None, None, None


def compare(countries, week):
    """Compares stats for multiple countries on the closest available date."""
    output = ""
    for country in countries:
        actual_date = get_closest_date(week, country, before=False)
        if actual_date:
            result = DataSource.get_sum_specific(country, week)
            
            """cursor = ds.connection.cursor()
            query = 
                SELECT SUM(New_cases), SUM(New_deaths)
                FROM bigTable
                WHERE Country = %s AND Date_reported = %s;
            
            cursor.execute(query, (country, actual_date))
            result = cursor.fetchone()
            cursor.close()"""

            total_cases = result[0] or 0
            total_deaths = result[1] or 0

            if week != actual_date:
                note = f"(Closest available date: {actual_date})"
            else:
                note = ""

            output += (
                f"Total cases in {country} on {actual_date}: {total_cases} {note}\n"
                f"Total deaths in {country} on {actual_date}: {total_deaths}\n\n"
            )
        else:
            output += f"No data available for {country} near {week}\n\n"

    return output

