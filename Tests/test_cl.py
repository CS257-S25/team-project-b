import unittest
from io import StringIO
import sys
import cl
from unittest import patch

class TestCL(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_compare_command_valid(self):
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn('Total cases in', output)

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
        self.assertIn('Total cases in', output)

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
        
    @patch('your_module_name.covid_stats.get_cases_and_deaths_stats')
    @patch('builtins.print')
    def test_handle_stats_data_found(self, mock_print, mock_get_stats):
        mock_get_stats.return_value = (1000, 50, "2023-01-01", "2023-01-31")
        cl.handle_stats("USA", "2023-01-01", "2023-01-31")
        mock_get_stats.assert_called_once_with("USA", "2023-01-01", "2023-01-31")
        mock_print.assert_called_once_with("""Total cases in USA from 2023-01-01 to 2023-01-31: 1000
Total deaths in USA from 2023-01-01 to 2023-01-31: 50""")

    @patch('your_module_name.covid_stats.get_cases_and_deaths_stats')
    @patch('builtins.print')
    def test_handle_stats_no_data(self, mock_print, mock_get_stats):
        mock_get_stats.return_value = (None, None, None, None)
        cl.handle_stats("Canada", "2023-02-01", "2023-02-15")
        mock_get_stats.assert_called_once_with("Canada", "2023-02-01", "2023-02-15")
        mock_print.assert_called_once_with("No data found for Canada in the given date range.")

if __name__ == '__main__':
    unittest.main()
