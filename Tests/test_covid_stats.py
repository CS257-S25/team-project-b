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
import unittest
from unittest.mock import MagicMock
from datetime import date
from ProductionCode import covid_stats

class MockDS:
    def get_all_data(self):
        return [
            {"Country": "Afghanistan", "Date_reported": date(2020, 3, 29), "New_cases": 67, "New_deaths": 2},
            {"Country": "Afghanistan", "Date_reported": date(2020, 3, 30), "New_cases": 3, "New_deaths": 0},
        ]

    def get_sum_between_dates(self, country, start_date, end_date):
        return (70, 2)

    def get_sum_specific(self, country, date):
        return (67, 2)

class TestCovidStats(unittest.TestCase):

    def test_get_closest_date_before(self):
        ds = MockDS()
        result = covid_stats.get_closest_date("2020-03-30", "Afghanistan", before=True, ds=ds)
        self.assertEqual(result, date(2020, 3, 30))

    def test_get_cases_and_deaths_stats(self):
        ds = MockDS()
        result = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-03-28", "2020-03-31", ds)
        self.assertEqual(result, (70, 2, date(2020, 3, 29), date(2020, 3, 30)))

    def test_compare(self):
        ds = MockDS()
        output, chart_data = covid_stats.compare(["Afghanistan"], "2020-03-29", ds)
        self.assertIn("Afghanistan on 2020-03-29", output)
        self.assertEqual(chart_data["labels"], ["Afghanistan"])
        self.assertEqual(chart_data["cases"], [67])
        self.assertEqual(chart_data["deaths"], [2])

if __name__ == '__main__':
    unittest.main()
