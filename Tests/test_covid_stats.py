"""import unittest
from ProductionCode import covid_stats
from datetime import date

class TestCovidStatsNoMock(unittest.TestCase):
    def test_to_date_valid_string(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_date_object(self):
        self.assertEqual(covid_stats.to_date(date(2020, 1, 1)), date(2020, 1, 1))

    def test_to_date_invalid_format(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("bad-date")

    def test_get_closest_date(self):
        result = covid_stats.get_closest_date("2020-01-01", "Afghanistan")
        self.assertIsInstance(result, date)

    def test_get_closest_date_no_match(self):
        result = covid_stats.get_closest_date("2020-01-01", "NonexistentCountry")
        self.assertIsNone(result)

    def test_get_cases_and_deaths_stats(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-12-31")
        self.assertIsInstance(cases, int)
        self.assertIsInstance(deaths, int)

    def test_get_cases_and_deaths_stats_no_data(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("NonexistentCountry", "2020-01-01", "2020-12-31")
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_compare_valid(self):
        text, data = covid_stats.compare(["Afghanistan", "Albania"], "2020-01-01")
        self.assertIn("cases", text)
        self.assertIn("deaths", text)

    def test_compare_no_data(self):
        text, data = covid_stats.compare(["NonexistentCountry"], "2020-01-01")
        self.assertIn("No data available", text)
        self.assertEqual(data["labels"], [])
        self.assertEqual(data["cases"], [])
        self.assertEqual(data["deaths"], [])

if __name__ == '__main__':
    unittest.main()"""
# test_covid_stats.py
import pytest
from datetime import date
from ProductionCode import covid_stats

class DummyDS:
    def __init__(self, all_data=None, sum_between=None, sum_specific=None):
        self._all_data = all_data or []
        self._sum_between = sum_between or (0, 0)
        self._sum_specific = sum_specific or (0, 0)
    def get_all_data(self):
        return self._all_data
    def get_sum_between_dates(self, country, start, end):
        return self._sum_between
    def get_sum_specific(self, country, date):
        return self._sum_specific

def test_to_date_valid_and_invalid():
    d = covid_stats.to_date("2020-01-01")
    assert d == date(2020, 1, 1)
    # Passing a date returns the same date
    today = date.today()
    assert covid_stats.to_date(today) == today
    with pytest.raises(ValueError):
        covid_stats.to_date("invalid-date")

def test_get_closest_date_before_and_after():
    data = [
        {"Country": "USA", "Date_reported": date(2020, 1, 1)},
        {"Country": "USA", "Date_reported": date(2020, 1, 3)},
        {"Country": "Canada", "Date_reported": date(2020, 1, 2)},
    ]
    ds = DummyDS(all_data=data)

    # before=True, date <= target date
    res = covid_stats.get_closest_date("2020-01-03", "USA", before=True, ds=ds)
    assert res == date(2020, 1, 3)

    # before=False, date >= target date
    res = covid_stats.get_closest_date("2020-01-02", "USA", before=False, ds=ds)
    assert res == date(2020, 1, 3)

    # No matching country
    res = covid_stats.get_closest_date("2020-01-01", "Mexico", ds=ds)
    assert res is None

def test_get_cases_and_deaths_stats_normal_and_none():
    data = [
        {"Country": "USA", "Date_reported": date(2020, 1, 1)},
        {"Country": "USA", "Date_reported": date(2020, 1, 10)},
    ]
    ds = DummyDS(all_data=data, sum_between=(100, 10))

    cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("USA", "2020-01-01", "2020-01-10", ds=ds)
    assert cases == 100
    assert deaths == 10
    assert start == date(2020, 1, 1)
    assert end == date(2020, 1, 10)

    # Simulate no data found for dates
    ds_no_data = DummyDS(all_data=[])
    cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("USA", "2020-01-01", "2020-01-10", ds=ds_no_data)
    assert cases is None and deaths is None and start is None and end is None

def test_compare_with_countries_and_edge_cases():
    all_data = [
        {"Country": "USA", "Date_reported": date(2020, 1, 7)},
        {"Country": "Canada", "Date_reported": date(2020, 1, 7)},
    ]
    ds = DummyDS(all_data=all_data, sum_specific=(5, 1))

    countries = ["USA", "Canada", "Mexico"]

    output, chart_data = covid_stats.compare(countries, "2020-01-01", ds=ds)
    assert "USA" in output
    assert "Canada" in output
    assert "Mexico" in output  # Mexico no data message
    assert "labels" in chart_data
    assert "cases" in chart_data
    assert "deaths" in chart_data
    assert set(chart_data["labels"]) == {"USA", "Canada"}

def test_compare_handles_zero_cases_and_no_data():
    ds = DummyDS(all_data=[{"Country": "USA", "Date_reported": date(2020, 1, 7)}],
                 sum_specific=(0, 0))
    output, _ = covid_stats.compare(["USA"], "2020-01-01", ds=ds)
    assert "No cases or deaths" in output

    ds_empty = DummyDS(all_data=[])
    output, _ = covid_stats.compare(["USA"], "2020-01-01", ds=ds_empty)
    assert "No data available" in output

