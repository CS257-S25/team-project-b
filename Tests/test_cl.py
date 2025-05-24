import unittest
from io import StringIO
import sys
# Import patch and MagicMock for mocking database interactions
from unittest.mock import patch, MagicMock
from datetime import date # Import date for mocking date objects

import cl
# We need to import covid_stats here, but its internal DataSource will be mocked.
from ProductionCode import covid_stats


# Patch ProductionCode.datasource.DataSource at the class level.
# This ensures that when DataSource() is instantiated anywhere (e.g., in covid_stats.py),
# it returns our mock object instead of trying to connect to a real database.
@patch('ProductionCode.datasource.DataSource')
class TestCovidStats(unittest.TestCase):
    """Unit tests for the command line interface (cl.py)."""

    def setUp(self, MockDataSource):
        """Set up the mock DataSource and configure its methods for each test."""
        # MockDataSource is the mock for the DataSource *class*.
        # We configure it to return a MagicMock instance when called.
        self.mock_ds_instance = MagicMock()
        MockDataSource.return_value = self.mock_ds_instance

        # Configure the return values for the methods that covid_stats will call on 'ds'.
        # These values are set to produce the '0' cases/deaths expected by existing CLI tests.
        self.mock_ds_instance.get_sum_between_dates.return_value = (0, 0) # (cases, deaths)
        self.mock_ds_instance.get_sum_specific.return_value = (0, 0) # (cases, deaths)
        self.mock_ds_instance.get_closest_date.side_effect = [
            date(2020, 1, 1), # For start date (before=False)
            date(2020, 1, 12), # For end date (before=True)
            date(2020, 1, 1), # For compare specific date
            date(2020, 1, 1) # For compare specific date (second country)
        ]
        # Ensure get_all_countries returns something if needed by actual code
        self.mock_ds_instance.get_all_countries.return_value = ["Afghanistan", "Albania", "USA"]

        # Store original sys.stdout and sys.argv to restore them after each test
        self.original_stdout = sys.stdout
        self.original_argv = sys.argv

    def tearDown(self):
        """Restore original stdout and argv after each test."""
        sys.stdout = self.original_stdout
        sys.argv = self.original_argv

    # Note: test_stats directly calls covid_stats.stats, which uses the mocked DataSource.
    def test_stats(self):
        """Test function for the stats function in covid_stats."""
        # The mock_ds_instance.get_sum_between_dates.return_value is already (0,0) from setUp.
        # The mock_ds_instance.get_closest_date.side_effect is also set up.
        self.assertEqual(
            covid_stats.get_cases_and_deaths_stats('Afghanistan', '2020-01-01', '2020-01-12'),
            (0, 0, date(2020, 1, 1), date(2020, 1, 12)) # Expecting actual_start, actual_end as dates
        )
        # Verify calls on the mocked DataSource methods
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-01-01', 'Afghanistan', before=False)
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-01-12', 'Afghanistan', before=True)
        self.mock_ds_instance.get_sum_between_dates.assert_called_with('Afghanistan', date(2020, 1, 1), date(2020, 1, 12))


    def test_handle_compare_invalid_args(self):
        """Test handle_compare with invalid arguments (missing date)"""
        sys.stdout = StringIO()
        # cl.handle_compare expects 2 arguments: countries_arg, week
        # Your test provides 'Afghanistan' and '2020-01-01'. This is actually 2 args.
        # The 'invalid args' case in cl.py is based on len(args) == 3 or len(args) == 4.
        # Let's adjust this test to reflect a true invalid argument count for handle_compare.
        # The current cl.handle_compare signature is (countries_arg, week).
        # If you meant to test the 'command' function's handling of invalid args,
        # that's covered by test_commands_with_invalid_args and test_cl_main_stats_not_enough_args.
        # For handle_compare, invalid args often means too many/few countries.
        
        # Test with too few countries (e.g., 1 country)
        cl.handle_compare('Afghanistan', '2020-01-01') # This will actually pass the country count check
        printed_output = sys.stdout.getvalue()
        # The 'Usage' string is printed if 2 <= len(countries) <= 5 is false.
        # For 'Afghanistan', len(['Afghanistan']) is 1, so it should print usage.
        self.assertIn("You must select between 2 and 5 countries.", printed_output)
        self.assertIn("Usage:", printed_output)

    def test_handle_compare_empty_countries(self):
        """Test handle_compare with empty countries string"""
        sys.stdout = StringIO()
        cl.handle_compare('', '2020-01-01')
        printed_output = sys.stdout.getvalue()
        self.assertIn("Usage:", printed_output)
        self.assertIn("You must select between 2 and 5 countries.", printed_output)


    def test_handle_compare_valid(self):
        """Test handle_compare with valid multiple countries and date"""
        sys.stdout = StringIO()
        # Reset side_effect for get_closest_date to ensure it's called for each country
        self.mock_ds_instance.get_closest_date.side_effect = [
            date(2020, 1, 1), # For Afghanistan
            date(2020, 1, 1)  # For Albania
        ]
        # Reset side_effect for get_sum_specific
        self.mock_ds_instance.get_sum_specific.side_effect = [
            (0, 0), # For Afghanistan
            (0, 0)  # For Albania
        ]

        cl.handle_compare('Afghanistan,Albania', '2020-01-01')
        printed_output = sys.stdout.getvalue()
        expected_output = (
            "Afghanistan on 2020-01-01: 0 cases, 0 deaths.\n\n"
            "Albania on 2020-01-01: 0 cases, 0 deaths.\n\n"
        )
        self.assertEqual(printed_output, expected_output)
        self.mock_ds_instance.get_sum_specific.assert_any_call("Afghanistan", date(2020, 1, 1))
        self.mock_ds_instance.get_sum_specific.assert_any_call("Albania", date(2020, 1, 1))


    def test_print_usage(self):
        """Test print_usage function output"""
        sys.stdout = StringIO()
        cl.print_usage()
        printed_output = sys.stdout.getvalue()
        # Updated expected usage string to match cl.py (removed 'highest')
        self.assertEqual(printed_output,
                         """Usage:
    python cl.py compare country1,country2,... date
    python cl.py stats country beginning_date ending_date
    """)

    def test_handle_stats(self):
        """Test handle_stats output for valid country and date range"""
        sys.stdout = StringIO()
        # Reset side_effect for get_closest_date for this specific test
        self.mock_ds_instance.get_closest_date.side_effect = [
            date(2020, 1, 1), # For beginning_date
            date(2020, 1, 12) # For ending_date
        ]
        # Reset return value for get_sum_between_dates for this specific test
        self.mock_ds_instance.get_sum_between_dates.return_value = (0, 0)

        cl.handle_stats('Afghanistan', '2020-01-01', '2020-01-12')
        printed_output = sys.stdout.getvalue()
        # The output format in cl.py is slightly different from your original test.
        # It uses 'Total cases in X from Y to Z: C\nTotal deaths in X from Y to Z: D'
        # Adjusted to match the actual cl.py output and remove the '!'
        self.assertEqual(printed_output,
                         """Total cases in Afghanistan from 2020-01-01 to 2020-01-12: 0
Total deaths in Afghanistan from 2020-01-01 to 2020-01-12: 0\n""")
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-01-01', 'Afghanistan', before=False)
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-01-12', 'Afghanistan', before=True)
        self.mock_ds_instance.get_sum_between_dates.assert_called_with('Afghanistan', date(2020, 1, 1), date(2020, 1, 12))


    def test_handle_stats_invalid_dates(self):
        """Test handle_stats with invalid date inputs (should print usage)"""
        sys.stdout = StringIO()
        # Mock get_closest_date to return None, simulating invalid date format
        self.mock_ds_instance.get_closest_date.side_effect = [None, date(2020, 1, 12)] # First call fails
        
        cl.handle_stats('Afghanistan', 'invalid-date', '2020-01-12')
        printed_output = sys.stdout.getvalue()
        # The error message from covid_stats.to_date will be printed, then usage.
        self.assertIn("Invalid date format: invalid-date. Expected YYYY-MM-DD.", printed_output)
        self.assertIn("Usage:", printed_output)


    def test_commands_with_invalid_args(self):
        """Test command() function with too many arguments"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12', '123']
        sys.stdout = StringIO()
        cl.command(sys.argv[1:])
        printed_output = sys.stdout.getvalue()
        # Updated expected usage string to match cl.py (removed 'highest')
        self.assertIn("Invalid command or wrong number of arguments.", printed_output)
        self.assertIn("Usage:", printed_output)


    def test_commands_with_unknown_command(self):
        """Test command() with unknown command"""
        sys.argv = ['cl.py', 'unknowncmd']
        sys.stdout = StringIO()
        cl.command(sys.argv[1:])
        printed_output = sys.stdout.getvalue()
        # Updated expected usage string to match cl.py (removed 'highest')
        self.assertIn("Invalid command or wrong number of arguments.", printed_output)
        self.assertIn("Usage:", printed_output)


    def test_cl_main_no_args(self):
        """Test main() with no command line arguments"""
        sys.argv = ['cl.py']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        # Updated expected usage string to match cl.py (removed 'highest')
        self.assertIn("Usage:", printed_output)


    def test_cl_main_stats_not_enough_args(self):
        """Test main() with stats command but missing dates"""
        sys.argv = ['cl.py', 'stats']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        # Updated expected usage string to match cl.py (removed 'highest')
        self.assertIn("Invalid command or wrong number of arguments.", printed_output)
        self.assertIn("Usage:", printed_output)


    def test_cl_main_stats(self):
        """Test main() with valid stats command and arguments"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        sys.stdout = StringIO()
        # Reset side_effect for get_closest_date for this specific test
        self.mock_ds_instance.get_closest_date.side_effect = [
            date(2020, 1, 1), # For beginning_date
            date(2020, 1, 12) # For ending_date
        ]
        # Reset return value for get_sum_between_dates for this specific test
        self.mock_ds_instance.get_sum_between_dates.return_value = (0, 0)

        cl.main()
        printed_output = sys.stdout.getvalue()
        # Adjusted to match the actual cl.py output and remove the '!'
        self.assertEqual(printed_output,
                         """Total cases in Afghanistan from 2020-01-01 to 2020-01-12: 0
Total deaths in Afghanistan from 2020-01-01 to 2020-01-12: 0\n""")
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-01-01', 'Afghanistan', before=False)
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-01-12', 'Afghanistan', before=True)
        self.mock_ds_instance.get_sum_between_dates.assert_called_with('Afghanistan', date(2020, 1, 1), date(2020, 1, 12))


    def test_cl_main_compare(self):
        """Test main() with valid compare command and arguments"""
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        sys.stdout = StringIO()
        # Reset side_effect for get_closest_date and get_sum_specific for this specific test
        self.mock_ds_instance.get_closest_date.side_effect = [
            date(2020, 1, 1), # For Afghanistan
            date(2020, 1, 1)  # For Albania
        ]
        self.mock_ds_instance.get_sum_specific.side_effect = [
            (0, 0), # For Afghanistan
            (0, 0)  # For Albania
        ]

        cl.main()
        printed_output = sys.stdout.getvalue()
        expected_output = (
            "Afghanistan on 2020-01-01: 0 cases, 0 deaths.\n\n"
            "Albania on 2020-01-01: 0 cases, 0 deaths.\n\n"
        )
        self.assertEqual(printed_output, expected_output)
        self.mock_ds_instance.get_sum_specific.assert_any_call("Afghanistan", date(2020, 1, 1))
        self.mock_ds_instance.get_sum_specific.assert_any_call("Albania", date(2020, 1, 1))


    def test_cl_main_unknown_command(self):
        """Test main() with unknown command"""
        sys.argv = ['cl.py', 'foobar']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        # Updated expected usage string to match cl.py (removed 'highest')
        self.assertIn("Invalid command or wrong number of arguments.", printed_output)
        self.assertIn("Usage:", printed_output)


if __name__ == '__main__':
    unittest.main()
