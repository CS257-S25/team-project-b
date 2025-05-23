"""Imports to run our tests"""
import unittest
from io import StringIO
import sys
import cl
from ProductionCode import covid_stats


class TestCovidStats(unittest.TestCase):
    """Class to hold our test functions for our command line"""

    def tearDown(self):
        """Reset stdout after each test"""
        sys.stdout = sys.__stdout__

    def test_stats(self):
        """Test function for the stats function"""
        self.assertEqual(
            covid_stats.stats('Afghanistan', '2020-01-01', '2020-01-12'), (0, 0))

    def test_handle_compare_invalid_args(self):
        """Test handle_compare with invalid arguments (missing date)"""
        sys.stdout = StringIO()
        cl.handle_compare('Afghanistan', '2020-01-01')
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output,
                         """Usage:\n
          python cl.py compare country1,country2..country5 date\n
          python cl.py stats country beginning_date ending_date\n
          python cl.py highest beginning_date ending_date\n""")

    def test_handle_compare_empty_countries(self):
        """Test handle_compare with empty countries string"""
        sys.stdout = StringIO()
        cl.handle_compare('', '2020-01-01')
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)

    def test_handle_compare_valid(self):
        """Test handle_compare with valid multiple countries and date"""
        sys.stdout = StringIO()
        cl.handle_compare('Afghanistan,Albania', '2020-01-01')
        printed_output = sys.stdout.getvalue()
        expected_output = (
            "Total cases in Afghanistan during 2020-01-01: 0\n"
            "          Total deaths in Afghanistan from 2020-01-01: 0\n"
            "Total cases in Albania during 2020-01-01: 0\n"
            "          Total deaths in Albania from 2020-01-01: 0\n\n"
        )
        self.assertEqual(printed_output, expected_output)

    def test_print_usage(self):
        """Test print_usage function output"""
        sys.stdout = StringIO()
        cl.print_usage()
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output,
                         """Usage:\n
          python cl.py compare country1,country2..country5 date\n
          python cl.py stats country beginning_date ending_date\n
          python cl.py highest beginning_date ending_date\n""")

    def test_handle_stats(self):
        """Test handle_stats output for valid country and date range"""
        sys.stdout = StringIO()
        cl.handle_stats('Afghanistan', '2020-01-01', '2020-01-12')
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output,
                         """Total cases in Afghanistan from 2020-01-01 to 2020-01-12: 0!\n
          Total deaths in Afghanistan from 2020-01-01 to 2020-01-12: 0!\n""")

    def test_handle_stats_invalid_dates(self):
        """Test handle_stats with invalid date inputs"""
        sys.stdout = StringIO()
        cl.handle_stats('Afghanistan', 'invalid-date', '2020-01-12')
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)

    def test_commands_with_invalid_args(self):
        """Test command() function with too many arguments"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12', '123']
        sys.stdout = StringIO()
        cl.command(sys.argv[1:])
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)

    def test_commands_with_unknown_command(self):
        """Test command() with unknown command"""
        sys.argv = ['cl.py', 'unknowncmd']
        sys.stdout = StringIO()
        cl.command(sys.argv[1:])
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)

    def test_cl_main_no_args(self):
        """Test main() with no command line arguments"""
        sys.argv = ['cl.py']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)

    def test_cl_main_stats_not_enough_args(self):
        """Test main() with stats command but missing dates"""
        sys.argv = ['cl.py', 'stats']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)

    def test_cl_main_stats(self):
        """Test main() with valid stats command and arguments"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output,
                         """Total cases in Afghanistan from 2020-01-01 to 2020-01-12: 0!\n
          Total deaths in Afghanistan from 2020-01-01 to 2020-01-12: 0!\n""")

    def test_cl_main_compare(self):
        """Test main() with valid compare command and arguments"""
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        expected_output = (
            "Total cases in Afghanistan during 2020-01-01: 0\n"
            "          Total deaths in Afghanistan from 2020-01-01: 0\n"
            "Total cases in Albania during 2020-01-01: 0\n"
            "          Total deaths in Albania from 2020-01-01: 0\n\n"
        )
        self.assertEqual(printed_output, expected_output)

    def test_cl_main_unknown_command(self):
        """Test main() with unknown command"""
        sys.argv = ['cl.py', 'foobar']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)


if __name__ == '__main__':
    unittest.main()
