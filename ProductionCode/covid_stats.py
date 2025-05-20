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
            if before and row_date <= target_date:
                dates.append(row_date)
            elif not before and row_date >= target_date:
                dates.append(row_date)

    if not dates:
        return None

    return max(dates) if before else min(dates)


def stats(country, beginning_date, ending_date):
    """Calculate total cases and deaths for a country between two dates."""
    beginning_date = to_date(beginning_date)
    ending_date = to_date(ending_date)

    start = get_closest_date(beginning_date, country, before=False)
    end = get_closest_date(ending_date, country, before=True)

    if not start or not end:
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
        date = get_closest_date(week, country, before=False)
        if not date:
            result += f"No data for {country}.\n\n"
            continue

        cases = 0
        deaths = 0

        for row in data:
            if row["Country"] == country and row["Date_reported"] == date:
                cases += row["New_cases"] or 0
                deaths += row["New_deaths"] or 0

        if cases == 0 and deaths == 0:
            result += f"{country} on {date}: No cases or deaths.\n\n"
        else:
            result += f"{country} on {date}: {cases} cases, {deaths} deaths.\n\n"

    return result
