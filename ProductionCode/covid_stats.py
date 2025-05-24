import unittest
from unittest.mock import MagicMock
from ProductionCode import covid_stats
from datetime import date, datetime

class TestCovidStats(unittest.TestCase):

    def setUp(self):
        # Create a mock DataSource object
        self.mock_ds = MagicMock()
        # Mock data for get_all_data()
        self.mock_ds.get_all_data.return_value = [
            {"Country": "Afghanistan", "Date_reported": date(2020, 1, 1), "New_cases": 10, "New_deaths": 1},
            {"Country": "Afghanistan", "Date_reported": date(2020, 1, 2), "New_cases": 5, "New_deaths": 0},
            {"Country": "Albania", "Date_reported": date(2020, 1, 1), "New_cases": 20, "New_deaths": 2},
        ]
        # Mock other DS methods
        self.mock_ds.get_sum_between_dates.return_value = (15, 1)
        self.mock_ds.get_sum_specific.return_value = (5, 0)

    # ----- to_date -----
    def test_to_date_valid_string(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_date_object(self):
        self.assertEqual(covid_stats.to_date(date(2020, 1, 1)), date(2020, 1, 1))

    def test_to_date_invalid_format(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("invalid-date")

    # ----- get_closest_date -----
    def test_get_closest_date_before_true(self):
        result = covid_stats.get_closest_date("2020-01-02", "Afghanistan", before=True, ds=self.mock_ds)
        self.assertEqual(result, date(2020, 1, 2))

    def test_get_closest_date_before_false(self):
        result = covid_stats.get_closest_date("2019-12-31", "Afghanistan", before=False, ds=self.mock_ds)
        self.assertEqual(result, date(2020, 1, 1))

    def test_get_closest_date_no_match(self):
        result = covid_stats.get_closest_date("2020-01-01", "NonexistentCountry", before=True, ds=self.mock_ds)
        self.assertIsNone(result)

    # ----- get_cases_and_deaths_stats -----
    def test_get_cases_and_deaths_stats_valid(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02", ds=self.mock_ds)
        self.assertEqual(cases, 15)
        self.assertEqual(deaths, 1)
        self.assertEqual(start, date(2020, 1, 1))
        self.assertEqual(end, date(2020, 1, 2))

    def test_get_cases_and_deaths_stats_no_data(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("NonexistentCountry", "2020-01-01", "2020-01-02", ds=self.mock_ds)
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_get_cases_and_deaths_stats_exception(self):
        self.mock_ds.get_sum_between_dates.side_effect = Exception("DB Error")
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02", ds=self.mock_ds)
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    # ----- compare -----
    def test_compare_valid(self):
        text, data = covid_stats.compare(["Afghanistan", "Albania"], "2020-01-01", ds=self.mock_ds)
        self.assertIn("Afghanistan", text)
        self.assertIn("Albania", text)
        self.assertIn("cases", text)
        self.assertIn("deaths", text)
        self.assertIn("Afghanistan", data["labels"])

    def test_compare_no_data(self):
        text, data = covid_stats.compare(["NonexistentCountry"], "2020-01-01", ds=self.mock_ds)
        self.assertIn("No data available", text)
        self.assertEqual(data["labels"], [])
        self.assertEqual(data["cases"], [])
        self.assertEqual(data["deaths"], [])

if __name__ == '__main__':
    unittest.main()
