import unittest
from unittest.mock import MagicMock
from datetime import date, datetime
from ProductionCode import covid_stats

class TestCovidStats(unittest.TestCase):
    def setUp(self):
        self.mock_ds = MagicMock()

    def test_to_date_with_valid_str(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_with_date_obj(self):
        d = date(2020, 1, 1)
        self.assertEqual(covid_stats.to_date(d), d)

    def test_to_date_invalid_str_raises(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("bad-date")

    def test_get_closest_date_before(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "Testland", "Date_reported": date(2020, 1, 1)},
            {"Country": "Testland", "Date_reported": date(2020, 1, 5)},
        ]
        result = covid_stats.get_closest_date("2020-01-04", "Testland", before=True, ds=self.mock_ds)
        self.assertEqual(result, date(2020, 1, 1))

    def test_get_closest_date_after(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "Testland", "Date_reported": date(2020, 1, 5)},
            {"Country": "Testland", "Date_reported": date(2020, 1, 10)},
        ]
        result = covid_stats.get_closest_date("2020-01-06", "Testland", before=False, ds=self.mock_ds)
        self.assertEqual(result, date(2020, 1, 10))

    def test_get_closest_date_none(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "Otherland", "Date_reported": date(2020, 1, 1)},
        ]
        result = covid_stats.get_closest_date("2020-01-01", "Nonexistent", ds=self.mock_ds)
        self.assertIsNone(result)

    def test_get_cases_and_deaths_stats_valid(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "Testland", "Date_reported": date(2020, 1, 1)},
            {"Country": "Testland", "Date_reported": date(2020, 1, 10)},
        ]
        self.mock_ds.get_sum_between_dates.return_value = (100, 5)
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Testland", "2020-01-01", "2020-01-10", ds=self.mock_ds)
        self.assertEqual(cases, 100)
        self.assertEqual(deaths, 5)
        self.assertEqual(start, date(2020, 1, 1))
        self.assertEqual(end, date(2020, 1, 10))

    def test_get_cases_and_deaths_stats_invalid_dates(self):
        self.mock_ds.get_all_data.return_value = []
        result = covid_stats.get_cases_and_deaths_stats("Testland", "2020-01-01", "2020-01-10", ds=self.mock_ds)
        self.assertEqual(result, (None, None, None, None))

    def test_get_cases_and_deaths_stats_exception(self):
        self.mock_ds.get_all_data.side_effect = KeyError("mock error")
        result = covid_stats.get_cases_and_deaths_stats("X", "2020-01-01", "2020-01-10", ds=self.mock_ds)
        self.assertEqual(result, (None, None, None, None))

    def test_compare_with_data(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "A", "Date_reported": date(2020, 1, 1)},
        ]
        self.mock_ds.get_sum_specific.return_value = (10, 2)
        output, chart_data = covid_stats.compare(["A"], "2020-01-01", ds=self.mock_ds)
        self.assertIn("A on", output)
        self.assertEqual(chart_data["labels"], ["A"])
        self.assertEqual(chart_data["cases"], [10])
        self.assertEqual(chart_data["deaths"], [2])

    def test_compare_no_data(self):
        self.mock_ds.get_all_data.return_value = []
        output, chart_data = covid_stats.compare(["Z"], "2020-01-01", ds=self.mock_ds)
        self.assertIn("No data available", output)
        self.assertEqual(chart_data["labels"], [])
        self.assertEqual(chart_data["cases"], [])
        self.assertEqual(chart_data["deaths"], [])

    def test_compare_zero_cases_deaths(self):
        self.mock_ds.get_all_data.return_value = [
            {"Country": "X", "Date_reported": date(2020, 1, 1)},
        ]
        self.mock_ds.get_sum_specific.return_value = (0, 0)
        output, chart_data = covid_stats.compare(["X"], "2020-01-01", ds=self.mock_ds)
        self.assertIn("No cases or deaths", output)
        self.assertEqual(chart_data["labels"], ["X"])
        self.assertEqual(chart_data["cases"], [0])
        self.assertEqual(chart_data["deaths"], [0])

if __name__ == "__main__":
    unittest.main()
