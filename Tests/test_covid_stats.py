import unittest
from unittest.mock import patch, MagicMock
from ProductionCode import covid_stats
from datetime import date, datetime

class TestCovidStats(unittest.TestCase):
    @patch('ProductionCode.covid_stats.DataSource')
    def setUp(self, mock_ds_class):
        # Create a mock DataSource instance
        self.mock_ds = MagicMock()
        mock_ds_class.return_value = self.mock_ds

        # Mock get_all_data
        self.mock_ds.get_all_data.return_value = [
            {"Country": "Afghanistan", "Date_reported": date(2020, 1, 1), "New_cases": 10, "New_deaths": 1},
            {"Country": "Afghanistan", "Date_reported": datetime(2020, 1, 2, 12, 0), "New_cases": 5, "New_deaths": 0},
            {"Country": "Albania", "Date_reported": date(2020, 1, 1), "New_cases": 20, "New_deaths": 2},
        ]
        self.mock_ds.get_sum_between_dates.return_value = (15, 1)
        self.mock_ds.get_sum_specific.return_value = (5, 0)

    # to_date tests
    def test_to_date_string(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_date_object(self):
        d = date(2020, 1, 1)
        self.assertEqual(covid_stats.to_date(d), d)

    def test_to_date_invalid(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("bad-date")

    # get_closest_date tests
    def test_get_closest_date_before_true(self):
        result = covid_stats.get_closest_date("2020-01-02", "Afghanistan", before=True)
        self.assertEqual(result, date(2020, 1, 2))

    def test_get_closest_date_before_false(self):
        result = covid_stats.get_closest_date("2020-01-01", "Afghanistan", before=False)
        self.assertEqual(result, date(2020, 1, 1))

    def test_get_closest_date_no_match(self):
        self.mock_ds.get_all_data.return_value = []
        result = covid_stats.get_closest_date("2020-01-01", "Nowhere", before=True)
        self.assertIsNone(result)

    def test_get_closest_date_datetime_conversion(self):
        result = covid_stats.get_closest_date("2020-01-02", "Afghanistan", before=True)
        self.assertIsInstance(result, date)

    # get_cases_and_deaths_stats tests
    def test_get_cases_and_deaths_stats_valid(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02")
        self.assertEqual(cases, 15)
        self.assertEqual(deaths, 1)
        self.assertEqual(start, date(2020, 1, 1))
        self.assertEqual(end, date(2020, 1, 2))

    def test_get_cases_and_deaths_stats_no_dates(self):
        self.mock_ds.get_all_data.return_value = []
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Nowhere", "2020-01-01", "2020-01-02")
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_get_cases_and_deaths_stats_exception(self):
        self.mock_ds.get_sum_between_dates.side_effect = Exception("DB Error")
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02")
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_get_cases_and_deaths_stats_none_result(self):
        self.mock_ds.get_sum_between_dates.return_value = (None, None)
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02")
        self.assertEqual(cases, 0)
        self.assertEqual(deaths, 0)

    # compare tests
    def test_compare_valid(self):
        text, data = covid_stats.compare(["Afghanistan", "Albania"], "2020-01-01")
        self.assertIn("Afghanistan", text)
        self.assertIn("Albania", text)
        self.assertIn("cases", text)
        self.assertIn("deaths", text)
        self.assertEqual(len(data["labels"]), 2)

    def test_compare_no_data(self):
        self.mock_ds.get_all_data.return_value = []
        text, data = covid_stats.compare(["Nowhere"], "2020-01-01")
        self.assertIn("No data available", text)
        self.assertEqual(data["labels"], [])
        self.assertEqual(data["cases"], [])
        self.assertEqual(data["deaths"], [])

    def test_compare_zero_cases(self):
        self.mock_ds.get_sum_specific.return_value = (0, 0)
        text, data = covid_stats.compare(["Afghanistan"], "2020-01-01")
        self.assertIn("No cases or deaths", text)

if __name__ == '__main__':
    unittest.main()
