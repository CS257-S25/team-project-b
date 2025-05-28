"""COVID-19 statistics functions."""

from datetime import datetime, date
from ProductionCode.datasource import DataSource

def to_date(date_str):
    """Convert a string to a date object."""
    if isinstance(date_str, date):
        return date_str
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.") from exc

def get_closest_date(target_date, country, before=True, ds=None):
    """Return the closest available date for a given country and direction."""
    if ds is None:
        raise ValueError("A DataSource instance must be provided to get_closest_date().")

    data = ds.get_all_data()
    target_date = to_date(target_date)
    dates = []

    for row in data:
        if row["Country"] != country:
            continue

        row_date = row["Date_reported"]
        if isinstance(row_date, datetime):
            row_date = row_date.date()

        if (before and row_date <= target_date) or (not before and row_date >= target_date):
            dates.append(row_date)

    if not dates:
        return None

    return max(dates) if before else min(dates)

def get_cases_and_deaths_stats(country, beginning_date, ending_date, ds):
    """Return total cases, deaths, and adjusted dates for a country."""
    start_date = get_closest_date(beginning_date, country, before=False, ds=ds)
    end_date = get_closest_date(ending_date, country, before=True, ds=ds)

    if not start_date or not end_date:
        return None, None, None, None

    result = ds.get_sum_between_dates(country, start_date, end_date)
    total_cases = result[0] or 0
    total_deaths = result[1] or 0

    return total_cases, total_deaths, start_date, end_date

def compare(countries, week, ds):
    """Compare total cases and deaths for each country in a selected week."""
    output = ""
    week_date = to_date(week)

    labels = []
    cases = []
    deaths = []

    for country in countries:
        actual_date = get_closest_date(week_date, country, before=False, ds=ds)
        if actual_date:
            result = ds.get_sum_specific(country, actual_date)
            total_cases = result[0] or 0
            total_deaths = result[1] or 0

            labels.append(country)
            cases.append(total_cases)
            deaths.append(total_deaths)

            if total_cases == 0 and total_deaths == 0:
                output += f"{country} on {actual_date}: No cases or deaths.\n\n"
            else:
                output += f"{country} on {actual_date}: {total_cases} cases, {total_deaths} deaths.\n\n"
        else:
            output += f"{country}: No data available on or after {week}.\n\n"

    chart_data = {
        "labels": labels,
        "cases": cases,
        "deaths": deaths
    }

    return output, chart_data
