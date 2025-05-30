"""Flask application for COVID-19 statistics"""
from flask import Flask, render_template, request
from ProductionCode.datasource import DataSource
from ProductionCode import covid_stats

app = Flask(__name__)

@app.route('/')
def homepage():
    """Homepage route that renders the main page."""
    return render_template('index.html')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    """Display COVID-19 statistics for a selected country and date range."""
    ds = DataSource()
    countries = ds.get_all_countries()
    chart_data = None
    total_cases = total_deaths = actual_start = actual_end = note = error = None

    if request.method == 'POST':
        country = request.form.get('country')
        beginning_date = request.form.get('beginning_date')
        ending_date = request.form.get('ending_date')

        stats_result = covid_stats.get_cases_and_deaths_stats(
            country, beginning_date, ending_date, ds=ds
        )
        total_cases, total_deaths, actual_start, actual_end = stats_result

        if total_cases is None:
            error = f"No data found for {country} near the dates you selected."
        else:
            if beginning_date != actual_start or ending_date != actual_end:
                note = f"Showing data from {actual_start} to {actual_end} (closest available dates)"

            daily_stats = ds.get_stats(country, actual_start, actual_end)
            chart_data = {
                "dates": [row[1].strftime("%Y-%m-%d") for row in daily_stats],
                "cases": [row[2] for row in daily_stats],
                "deaths": [row[3] for row in daily_stats],
            }

    return render_template(
        'stats.html',
        countries=countries,
        country=country if request.method == 'POST' else None,
        start=actual_start,
        end=actual_end,
        cases=total_cases,
        deaths=total_deaths,
        note=note,
        error=error,
        chart_data=chart_data
    )

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    """Compare COVID-19 statistics for multiple countries on a specific week."""
    ds = DataSource()
    countries = ds.get_all_countries()
    chart_data = None
    result = None
    week = None

    if request.method == 'POST':
        selected_countries = request.form.getlist('countries')
        week = request.form.get('week')

        result, chart_data = covid_stats.compare(selected_countries, week, ds=ds)

    return render_template(
        'compare.html',
        countries=countries,
        result=result,
        week=week,
        chart_data=chart_data
    )

@app.route('/help')
def help_page():
    """Display help information for the application."""
    return render_template('help.html')

@app.errorhandler(404)
def page_not_found(_e):
    """Custom 404 error page."""
    return render_template('404.html', error_message="Page not found!"), 404

if __name__ == '__main__':
    app.run(port=5004, debug=True)
    app.run(port=5253, debug=True)
