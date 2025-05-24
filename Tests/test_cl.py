"""import unittest
from io import StringIO
import sys
import cl
from datetime import date
from ProductionCode import covid_stats

class TestCL(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    # ----- CLI Tests -----
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
        self.assertIn('Total cases in Afghanistan', output)

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

    # ----- covid_stats Tests -----
    def test_to_date_valid_string(self):
        self.assertEqual(covid_stats.to_date("2020-01-01"), date(2020, 1, 1))

    def test_to_date_date_object(self):
        self.assertEqual(covid_stats.to_date(date(2020, 1, 1)), date(2020, 1, 1))

    def test_to_date_invalid_format(self):
        with self.assertRaises(ValueError):
            covid_stats.to_date("invalid-date")

    def test_get_closest_date_before_true(self):
        result = covid_stats.get_closest_date("2020-01-01", "Afghanistan", before=True)
        self.assertIsInstance(result, date)

    def test_get_closest_date_before_false(self):
        result = covid_stats.get_closest_date("2020-01-01", "Afghanistan", before=False)
        self.assertIsInstance(result, date)

    def test_get_closest_date_no_match(self):
        result = covid_stats.get_closest_date("2020-01-01", "NonexistentCountry")
        self.assertIsNone(result)

    def test_get_cases_and_deaths_stats_valid(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("Afghanistan", "2020-01-01", "2020-01-12")
        self.assertIsInstance(cases, int)
        self.assertIsInstance(deaths, int)

    def test_get_cases_and_deaths_stats_no_data(self):
        cases, deaths, start, end = covid_stats.get_cases_and_deaths_stats("NonexistentCountry", "2020-01-01", "2020-01-12")
        self.assertIsNone(cases)
        self.assertIsNone(deaths)

    def test_compare_valid(self):
        text, data = covid_stats.compare(["Afghanistan", "Albania"], "2020-01-01")
        self.assertIn("Total cases", text)
        self.assertIn("Afghanistan", data["labels"])

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
import io
import sys

class TestCL(unittest.TestCase):

    @patch('builtins.print')
    def test_print_usage(self, mock_print):
        import cl
        cl.print_usage()
        self.assertTrue(mock_print.called)

    @patch('cl.covid_stats.compare')
    @patch('builtins.print')
    def test_handle_compare(self, mock_print, mock_compare):
        mock_compare.return_value = ("comparison output", {})
        import cl
        cl.handle_compare("CountryA,CountryB", "2020-01-01")
        mock_print.assert_called_with("comparison output")

    @patch('cl.covid_stats.get_cases_and_deaths_stats')
    @patch('builtins.print')
    def test_handle_stats_with_data(self, mock_print, mock_get_stats):
        mock_get_stats.return_value = (100, 5, "2020-01-01", "2020-01-10")
        import cl
        cl.handle_stats("CountryA", "2020-01-01", "2020-01-10")
        self.assertTrue(any("Total cases" in call.args[0] for call in mock_print.call_args_list))

    @patch('cl.covid_stats.get_cases_and_deaths_stats')
    @patch('builtins.print')
    def test_handle_stats_no_data(self, mock_print, mock_get_stats):
        mock_get_stats.return_value = (None, None, None, None)
        import cl
        cl.handle_stats("CountryA", "2020-01-01", "2020-01-10")
        self.assertTrue(any("No data" in call.args[0] for call in mock_print.call_args_list))

    @patch('builtins.print')
    def test_main_with_invalid_args(self, mock_print):
        import cl
        testargs = ["cl.py"]
        with patch('sys.argv', testargs):
            cl.main()
        self.assertTrue(any("Usage" in call.args[0] for call in mock_print.call_args_list))

    # Add more tests for main with valid commands if needed

if __name__ == '__main__':
    unittest.main()
