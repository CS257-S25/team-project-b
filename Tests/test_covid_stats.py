import unittest
from ProductionCode import covid_stats
from datetime import date

class TestCovidStats(unittest.TestCase):
    def test_to_date_valid_string(self):
        result = covid_stats.to_date("2020-01-01")
        self.assertEqual(result, date(2020, 1, 1))

    def test_to_date_invalid_string(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("invalid-date")

    def test_get_closest_date(self):
        result = covid_stats.get_closest_date("2020-01-01", "Afghanistan")
        self.assertIsNotNone(result)

    def test_get_cases_and_deaths_stats_valid(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-12")
        self.assertIsNotNone(cases)
        self.assertIsNotNone(deaths)

    def test_get_cases_and_deaths_stats_invalid(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("NonexistentCountry", "2020-01-01", "2020-01-12")
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_compare_valid(self):
        text, data = covid_stats.compare(["Afghanistan", "Albania"], "2020-01-01")
        self.assertIn("Total cases", text)

    def test_compare_no_data(self):
        text, data = covid_stats.compare(["NonexistentCountry"], "2020-01-01")
        self.assertIn("No data available", text)

if __name__ == '__main__':
    unittest.main()
