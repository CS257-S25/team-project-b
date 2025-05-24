import unittest
from unittest.mock import patch, MagicMock
from datetime import date, datetime
from ProductionCode import covid_stats

class TestCovidStats(unittest.TestCase):

    @patch('ProductionCode.covid_stats.DataSource')
    def setUp(self, mock_ds_class):
        # Create a MagicMock instance for the DataSource
        self.mock_ds_instance = MagicMock()
        mock_ds_class.return_value = self.mock_ds_instance

        # Set up default return values
        self.mock_ds_instance.get_all_data.return_value = [
            {"Country": "Afghanistan", "Date_reported": date(2020, 1, 1), "New_cases": 10, "New_deaths": 1},
            {"Country": "Afghanistan", "Date_reported": datetime(2020, 1, 2, 12), "New_cases": 5, "New_deaths": 0},
            {"Country": "Albania", "Date_reported": date(2020, 1, 1), "New_cases": 20, "New_deaths": 2}
        ]
        self.mock_ds_instance.get_sum_between_dates.return_value = (15, 1)
        self.mock_ds_instance.get_sum_specific.return_value = (5, 0)

    def test_to_date_string(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_date_object(self):
        d = date(2020, 1, 1)
        self.assertEqual(covid_stats.to_date(d), d)

    def test_to_date_invalid(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("invalid")

    def test_get_closest_date_before_true(self):
        result = covid_stats.get_closest_date("2020-01-02", "Afghanistan", before=True)
        self.assertEqual(result, date(2020, 1, 2))

    def test_get_closest_date_before_false(self):
        result = covid_stats.get_closest_date("2020-01-01", "Afghanistan", before=False)
        self.assertEqual(result, date(2020, 1, 1))

    def test_get_closest_date_no_data(self):
        self.mock_ds_instance.get_all_data.return_value = []
        result = covid_stats.get_closest_date("2020-01-01", "NoCountry", before=True)
        self.assertIsNone(result)

    def test_get_cases_and_deaths_stats_valid(self):
        result = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02")
        self.assertEqual(result, (15, 1, date(2020, 1, 1), date(2020, 1, 2)))

    def test_get_cases_and_deaths_stats_none_dates(self):
        self.mock_ds_instance.get_all_data.return_value = []
        result = covid_stats.get_cases_and_deaths_stats("Ghostland", "2020-01-01", "2020-01-02")
        self.assertEqual(result, (None, None, None, None))

    def test_get_cases_and_deaths_stats_error(self):
        self.mock_ds_instance.get_sum_between_dates.side_effect = Exception("error")
        result = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02")
        self.assertEqual(result, (None, None, None, None))

    def test_get_cases_and_deaths_stats_none_result(self):
        self.mock_ds_instance.get_sum_between_dates.return_value = (None, None)
        result = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-02")
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)

    def test_compare_valid(self):
        text, data = covid_stats.compare(["Afghanistan", "Albania"], "2020-01-01")
        self.assertIn("Afghanistan", text)
        self.assertIn("Albania", text)
        self.assertEqual(data["labels"], ["Afghanistan", "Albania"])

    def test_compare_no_data(self):
        self.mock_ds_instance.get_all_data.return_value = []
        text, data = covid_stats.compare(["NoCountry"], "2020-01-01")
        self.assertIn("No data available", text)
        self.assertEqual(data["labels"], [])
        self.assertEqual(data["cases"], [])
        self.assertEqual(data["deaths"], [])

    def test_compare_zero_case_death(self):
        self.mock_ds_instance.get_sum_specific.return_value = (0, 0)
        text, _ = covid_stats.compare(["Afghanistan"], "2020-01-01")
        self.assertIn("No cases or deaths", text)

if __name__ == '__main__':
    unittest.main()
