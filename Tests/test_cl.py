import unittest
from io import StringIO
import sys
import cl
from datetime import date

class TestCL(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    # ----- CLI tests -----
    def test_compare_command_valid(self):
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn('Total cases', output)

    def test_compare_command_missing_args(self):
        sys.argv = ['cl.py', 'compare', 'Afghanistan']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_compare_command_too_many_countries(self):
        sys.argv = ['cl.py', 'compare', 'A,B,C,D,E,F', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_stats_command_valid(self):
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn('Total cases', output)

    def test_stats_command_missing_args(self):
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_stats_command_extra_args(self):
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12', 'extra']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Invalid command", output)

    def test_no_command(self):
        sys.argv = ['cl.py']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_unknown_command(self):
        sys.argv = ['cl.py', 'foobar']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Invalid command", output)

    # ----- covid_stats.to_date tests -----
    def test_to_date_valid_string(self):
        from ProductionCode import covid_stats
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_date_object(self):
        from ProductionCode import covid_stats
        self.assertEqual(covid_stats.to_date(date(2020, 1, 1)), date(2020, 1, 1))

    def test_to_date_invalid_format(self):
        from ProductionCode import covid_stats
        with self.assertRaises(ValueError):
            covid_stats.to_date("invalid-date")

    # ----- covid_stats edge cases -----
    def test_get_cases_and_deaths_stats_none_case(self):
        from ProductionCode import covid_stats
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("NonexistentCountry", "2020-01-01", "2020-01-12")
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_compare_no_data(self):
        from ProductionCode import covid_stats
        text, data = covid_stats.compare(["NonexistentCountry"], "2020-01-01")
        self.assertIn("No data available", text)
        self.assertEqual(data["labels"], [])
        self.assertEqual(data["cases"], [])
        self.assertEqual(data["deaths"], [])

if __name__ == '__main__':
    unittest.main()
