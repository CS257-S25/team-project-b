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
from unittest.mock import patch, MagicMock
from ProductionCode import covid_stats

class TestCovidStats(unittest.TestCase):
    def setUp(self):
        patcher = patch('ProductionCode.covid_stats.DataSource')
        self.mock_ds_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_ds_instance = self.mock_ds_class.return_value

    def test_get_total_cases_and_deaths_normal(self):
        self.mock_ds_instance.get_sum_between_dates.return_value = (1000, 200)
        cases, deaths = covid_stats.get_total_cases_and_deaths("USA", "2021-01-01", "2021-01-10")
        self.assertEqual(cases, 1000)
        self.assertEqual(deaths, 200)
        self.mock_ds_instance.get_sum_between_dates.assert_called_once_with("USA", "2021-01-01", "2021-01-10")

    def test_get_total_cases_and_deaths_none_values(self):
        # None values should become 0
        self.mock_ds_instance.get_sum_between_dates.return_value = (None, None)
        cases, deaths = covid_stats.get_total_cases_and_deaths("USA", "2021-01-01", "2021-01-10")
        self.assertEqual(cases, 0)
        self.assertEqual(deaths, 0)

    def test_calculate_case_fatality_rate_normal(self):
        rate = covid_stats.calculate_case_fatality_rate(1000, 50)
        self.assertAlmostEqual(rate, 5.0)

    def test_calculate_case_fatality_rate_zero_cases(self):
        # Should not divide by zero
        rate = covid_stats.calculate_case_fatality_rate(0, 50)
        self.assertEqual(rate, 0.0)

    def test_format_summary_string_output(self):
        summary = covid_stats.format_summary_string("USA", 1000, 50, 5.0)
        expected = "COVID-19 summary for USA:\nTotal cases: 1000\nTotal deaths: 50\nCFR: 5.00%"
        self.assertEqual(summary, expected)

if __name__ == '__main__':
    unittest.main()

