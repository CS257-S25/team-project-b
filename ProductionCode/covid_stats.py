"""Provides simple COVID-19 statistics functions."""

from .datasource import DataSource
from datetime import datetime, date

ds = DataSource()

def to_date(date_str):
    """Convert a string to a date object."""
    if isinstance(date_str, date):
        return date_str
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")

        
def get_closest_date(target_date, country, before=True):
    """Return closest available date for a country."""
    data = ds.get_all_data()
    target_date = to_date(target_date)
    dates = []

    for row in data:
        if row["Country"] == country:
            row_date = row["Date_reported"]
            # Ensure the row_date is a date object
            if isinstance(row_date, datetime):
                row_date = row_date.date()

            if before and row_date <= target_date:
                dates.append(row_date)
            elif not before and row_date >= target_date:
                dates.append(row_date)

    if not dates:
        return None

    return max(dates) if before else min(dates)


def stats(country, beginning_date, ending_date):
    """Calculates total cases and deaths using closest available dates."""
    try:
        start_date = get_closest_date(beginning_date, country, before=False)
        end_date = get_closest_date(ending_date, country, before=True)

        if not start_date or not end_date:
            return None, None, None, None  # No valid range

        cursor = ds.connection.cursor()
        cursor.execute(query, (country, start_date, end_date))
        result = cursor.fetchone()
        cursor.close()

        total_cases = result[0] or 0
        total_deaths = result[1] or 0

        return total_cases, total_deaths, start_date, end_date

    except Exception as e:
        print("Error in stats():", e)
        return None, None, None, None

    data = ds.get_all_data()
    total_cases = 0
    total_deaths = 0

    for row in data:
        if row["Country"] == country:
            date = row["Date_reported"]
            if start <= date <= end:
                total_cases += row["New_cases"] or 0
                total_deaths += row["New_deaths"] or 0

    return total_cases, total_deaths, start, end


def compare(countries, week):
    """Compare total cases and deaths for each country on a given week."""
    data = ds.get_all_data()
    result = ""
    week = to_date(week)

    for country in countries:
        actual_date = get_closest_date(week, country, before=False)
        if actual_date:
            result = DataSource.get_sum_specific(country, week)
            
            cursor.execute(query, (country, actual_date))
            result = cursor.fetchone()
            cursor.close()

            total_cases = result[0] or 0
            total_deaths = result[1] or 0

        if cases == 0 and deaths == 0:
            result += f"{country} on {date}: No cases or deaths.\n\n"
        else:
            result += f"{country} on {date}: {cases} cases, {deaths} deaths.\n\n"

    return result
