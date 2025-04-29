"""Flask app to show COVID-19 statistics."""

from flask import Flask
from ProductionCode import covid_stats

app = Flask(__name__)

@app.route('/')
def homepage():
    """Show homepage instructions."""
    return (
        "<h1>Hello, this is the homepage.</h1>"
        "- To get COVID-19 statistics, use this URL format:"
        "/stats/<country>/<beginning_date>/<ending_date>"
        "Example:\n"
        "/stats/USA/2020-03-01/2020-03-10<br>"
        "- please use this format to compare: /compare///"
        "\nExample:\n"
        "/compare/2020-04-19/US,GB"

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
    
@app.route('/compare/<date>/<countries>')
def compare(date, countries):
    """This function compares COVID-19 stats for multiple countries using one date"""
    try:
        output = f"COVID-19 data for {date}:\n"
        for country in countries.split(','):
            cases, deaths = covid_stats.stats(country, date, date)
            output += f"{country}: Cases={cases}, Deaths={deaths}\n"
        return output
    except (ValueError, KeyError) as e:
        return f"Error: {str(e)}"
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors with a custom message."""
    
    return (""
    "<h1>Error 404: The requested resource was not found.</h1>"
        "- To get COVID-19 statistics, use this URL format:"
        "/stats/<country>/<beginning_date>/<ending_date>"
        "Example:\n"
        "/stats/USA/2020-03-01/2020-03-10<br>"
        "- please use this format to compare: /compare///"
        "\nExample:\n"
        "/compare/2020-04-19/US,GB", 404)


if __name__ == '__main__':
    app.run(debug=True,port=5001)
