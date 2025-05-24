import unittest
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
    unittest.main()
