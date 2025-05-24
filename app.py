'''Modules to run our flask app'''
from flask import Flask, render_template, request
from ProductionCode import covid_stats
from ProductionCode.datasource import DataSource

app = Flask(__name__)

@app.route('/')
def homepage():
    '''Homepage of our website'''
    return render_template('index.html')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    '''Page to show the covid statistics of a country'''
    ds = DataSource()
    countries = ds.get_all_countries()
    if request.method == 'POST':
        country = request.form.get('country')
        beginning_date = request.form.get('beginning_date')
        ending_date = request.form.get('ending_date')

        total_cases, total_deaths, actual_start, = \
            actual_end = covid_stats.get_cases_and_deaths_stats(
            country, beginning_date, ending_date
        )

        if total_cases is None:
            error = f"No data found for {country} near the dates you selected."
            return render_template('stats.html', countries=countries, error=error)

        note = ""
        if beginning_date != actual_start or ending_date != actual_end:
            note = f"Showing data from {actual_start} to {actual_end} (closest available dates)."

        return render_template('stats.html', countries=countries, country=country,
                               start=actual_start, end=actual_end,
                               cases=total_cases, deaths=total_deaths, note=note)

    return render_template('stats.html', countries=countries)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    '''Compare page for the covid statistic of multiple countries'''
    ds = DataSource()
    countries = ds.get_all_countries()
    if request.method == 'POST':
        selected_countries = request.form.getlist('countries')
        week = request.form.get('week')

        comparison_result, chart_data = covid_stats.compare(selected_countries, week)

        return render_template('compare.html', countries=countries,
                               result=comparison_result, week=week, chart_data=chart_data)

    return render_template('compare.html', countries=countries)

@app.route('/help')
def help_page():
    '''Help page'''
    return render_template('help.html')

@app.errorhandler(404)
def page_not_found(e):
    '''Error page for 404'''
    return render_template('404.html', error_message=f"{e}, is the error. Page not found!"), 404

if __name__ == '__main__':
    app.run()
