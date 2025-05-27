import unittest
from io import StringIO
import sys
from unittest.mock import patch
import cl


class TestCL(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        self.original_argv = sys.argv[:]

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.argv = self.original_argv

    @patch('ProductionCode.covid_stats.compare')
    def test_compare_command_valid(self, mock_compare):
        mock_compare.return_value = ("Total cases in Afghanistan and Albania", {'labels': ['Afghanistan', 'Albania']})
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Total cases in Afghanistan and Albania", output)
        mock_compare.assert_called_once()

    def test_compare_command_too_few_countries(self):
        sys.argv = ['cl.py', 'compare', 'Afghanistan', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("You must select between 2 and 5 countries", output)

    def test_compare_command_too_many_countries(self):
        sys.argv = ['cl.py', 'compare', 'A,B,C,D,E,F', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("You must select between 2 and 5 countries", output)

    def test_compare_command_missing_args(self):
        sys.argv = ['cl.py', 'compare', 'Afghanistan']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_compare_command_empty_country_list(self):
        sys.argv = ['cl.py', 'compare', '', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("You must select between 2 and 5 countries", output)

    @patch('ProductionCode.covid_stats.get_cases_and_deaths_stats')
    def test_stats_command_valid(self, mock_stats):
        mock_stats.return_value = (1234, 56, '2020-01-01', '2020-01-10')
        sys.argv = ['cl.py', 'stats', 'USA', '2020-01-01', '2020-01-10']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Total cases in USA from 2020-01-01 to 2020-01-10: 1234", output)
        self.assertIn("Total deaths in USA from 2020-01-01 to 2020-01-10: 56", output)

    @patch('ProductionCode.covid_stats.get_cases_and_deaths_stats')
    def test_stats_command_no_data(self, mock_stats):
        mock_stats.return_value = (None, None, None, None)
        sys.argv = ['cl.py', 'stats', 'USA', '2020-01-01', '2020-01-10']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("No data found for USA", output)

    def test_stats_command_missing_args(self):
        sys.argv = ['cl.py', 'stats', 'USA', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_invalid_command(self):
        sys.argv = ['cl.py', 'invalidcmd', 'foo', 'bar']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Invalid command or wrong number of arguments", output)
        self.assertIn("Usage:", output)

    def test_no_command(self):
        sys.argv = ['cl.py']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)


if __name__ == '__main__':
    unittest.main()
