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
# test_cl.py
import pytest
from unittest.mock import patch
import ProductionCode.cl as cl

def test_print_usage(capsys):
    cl.print_usage()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out

@patch("ProductionCode.cl.covid_stats.compare")
def test_handle_compare_valid_and_invalid(mock_compare, capsys):
    mock_compare.return_value = ("result", {"labels": [], "cases": [], "deaths": []})

    cl.handle_compare("USA,Canada", "2020-01-01")
    captured = capsys.readouterr()
    assert "result" in captured.out

    cl.handle_compare("USA", "2020-01-01")  # less than 2 countries
    captured = capsys.readouterr()
    assert "You must select between 2 and 5 countries." in captured.out

    cl.handle_compare("USA,Canada,Mexico,Brazil,France,Spain", "2020-01-01")  # more than 5
    captured = capsys.readouterr()
    assert "You must select between 2 and 5 countries." in captured.out

@patch("ProductionCode.cl.covid_stats.get_cases_and_deaths_stats")
def test_handle_stats_found_and_not_found(mock_stats, capsys):
    mock_stats.return_value = (100, 10, "2020-01-01", "2020-01-10")
    cl.handle_stats("USA", "2020-01-01", "2020-01-10")
    captured = capsys.readouterr()
    assert "Total cases in USA" in captured.out

    mock_stats.return_value = (None, None, None, None)
    cl.handle_stats("USA", "2020-01-01", "2020-01-10")
    captured = capsys.readouterr()
    assert "No data found for USA" in captured.out

def test_command_dispatch(capsys):
    cl.command([])
    captured = capsys.readouterr()
    assert "Usage:" in captured.out

    with patch("ProductionCode.cl.handle_compare") as mock_compare:
        cl.command(["compare", "USA,Canada", "2020-01-01"])
        mock_compare.assert_called_once_with("USA,Canada", "2020-01-01")

    with patch("ProductionCode.cl.handle_stats") as mock_stats:
        cl.command(["stats", "USA", "2020-01-01", "2020-01-10"])
        mock_stats.assert_called_once_with("USA", "2020-01-01", "2020-01-10")

    cl.command(["invalid"])
    captured = capsys.readouterr()
    assert "Invalid command" in captured.out
