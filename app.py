from flask import Flask, render_template, request
from ProductionCode import covid_stats
from ProductionCode.datasource import DataSource

app = Flask(__name__)
ds = DataSource()
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    countries = ds.get_all_countries()  # Get countries from DB

    if request.method == 'POST':
        country = request.form.get('country')
        beginning_date = request.form.get('beginning_date')
        ending_date = request.form.get('ending_date')

        try:
            total_cases, total_deaths = covid_stats.stats(country, beginning_date, ending_date)
            return render_template('stats.html', countries=countries, country=country,
                                   start=beginning_date, end=ending_date,
                                   cases=total_cases, deaths=total_deaths)
        except (ValueError, KeyError) as e:
            return render_template('404.html', error_message=str(e)), 404

    return render_template('stats.html', countries=countries, country=None)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        date = request.form.get('date')
        countries = request.form.get('countries')
        try:
            compare_data = covid_stats.compare(countries.split(','), date)
            return render_template('compare.html', date=date, countries=countries, results=compare_data)
        except (ValueError, KeyError) as e:
            return render_template('404.html', error_message=str(e)), 404
    return render_template('compare.html', results=None)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_message="Page not found!"), 404

if __name__ == '__main__':
    app.run(debug=True)
