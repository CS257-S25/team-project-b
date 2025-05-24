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

class TestCovidStats(unittest.TestCase):
    def setUp(self):
        self.mock_ds = MagicMock()

    def test_to_date_with_date_obj(self):
        d = date(2020, 1, 1)
        self.assertEqual(covid_stats.to_date(d), d)

    def test_to_date_with_valid_string(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020,1,1))

    def test_to_date_with_invalid_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("not-a-date")

    def test_get_closest_date_before(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "A", "Date_reported": date(2020,1,1)},
            {"Country": "A", "Date_reported": date(2020,1,5)},
        ]
        result = covid_stats.get_closest_date("2020-01-03", "A", before=True, ds=self.mock_ds)
        self.assertEqual(result, date(2020,1,1))

    def test_get_closest_date_after(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "A", "Date_reported": date(2020,1,1)},
            {"Country": "A", "Date_reported": date(2020,1,5)},
        ]
        result = covid_stats.get_closest_date("2020-01-03", "A", before=False, ds=self.mock_ds)
        self.assertEqual(result, date(2020,1,5))

    def test_get_cases_and_deaths_stats_returns_data(self):
        self.mock_ds.get_sum_between_dates.return_value = (100, 5)
        self.mock_ds.get_all_data.return_value = [
            {"Country": "A", "Date_reported": date(2020,1,1)},
            {"Country": "A", "Date_reported": date(2020,1,10)},
        ]
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("A", "2020-01-01", "2020-01-10", ds=self.mock_ds)
        self.assertEqual(cases, 100)
        self.assertEqual(deaths, 5)
        self.assertEqual(start, date(2020,1,1))
        self.assertEqual(end, date(2020,1,10))

    def test_get_cases_and_deaths_stats_no_data(self):
        self.mock_ds.get_sum_between_dates.return_value = (None, None)
        self.mock_ds.get_all_data.return_value = []
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("A", "2020-01-01", "2020-01-10", ds=self.mock_ds)
        self.assertIsNone(cases)
        self.assertIsNone(deaths)
        self.assertIsNone(start)
        self.assertIsNone(end)

if __name__ == '__main__':
    unittest.main()
