"""Flask app to show COVID-19 statistics."""

from flask import Flask
from ProductionCode import covid_stats

app = Flask(__name__)

@app.route('/')
def homepage():
    """Show homepage instructions."""
    return (
        "Hello, this is the homepage.\n\n"
        "To get COVID-19 statistics, use this URL format:\n"
        "/stats/<country>/<beginning_date>/<ending_date>\n"
        "Example:\n"
        "/stats/USA/2020-03-01/2020-03-10"
    )

@app.route("/stats/<country>/<beginning_date>/<ending_date>", strict_slashes=False)
def stats(country, beginning_date, ending_date):
    """Show COVID-19 stats for a country between two dates."""
    try:
        total_cases, total_deaths = covid_stats.stats(country, beginning_date, ending_date)
        return (
            f"COVID-19 stats for {country} from {beginning_date} to {ending_date}:\n"
            f"Total Cases: {total_cases}\n"
            f"Total Deaths: {total_deaths}"
        )
    except (ValueError, KeyError) as e:
        return f"Error: Invalid input or missing data. {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
