import unittest
from unittest.mock import patch
import sys
from io import StringIO
import cl

class TestCL(unittest.TestCase):
    """Unit tests for the cl.py command-line interface."""

    def setUp(self):
        """Set up mock sys.stdout for capturing print outputs."""
        self.held_stdout = StringIO()
        self.patcher = patch('sys.stdout', self.held_stdout)
        self.patcher.start()

    def tearDown(self):
        """Restore sys.stdout after each test."""
        self.patcher.stop()
        self.held_stdout.close()

    @patch('ProductionCode.covid_stats.compare')
    def test_compare_command_valid(self, mock_compare):
        """Test the compare command with valid input."""
        mock_compare.return_value = ("Mock comparison text", {"labels": [], "cases": [], "deaths": []})
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        cl.main()
        output = self.held_stdout.getvalue()
        self.assertIn("Mock comparison text", output)

    @patch('ProductionCode.covid_stats.get_cases_and_deaths_stats')
    def test_stats_command_valid(self, mock_stats):
        """Test the stats command with valid input."""
        mock_stats.return_value = (100, 5, '2020-01-01', '2020-01-12')
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        cl.main()
        output = self.held_stdout.getvalue()
        self.assertIn("Total cases in Afghanistan", output)
        self.assertIn("100", output)

    def test_stats_command_invalid_args(self):
        """Test the stats command with missing arguments."""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01']
        cl.main()
        output = self.held_stdout.getvalue()
        self.assertIn("Usage:", output)

    def test_compare_command_missing_args(self):
        """Test the compare command with missing arguments."""
        sys.argv = ['cl.py', 'compare', 'Afghanistan']
        cl.main()
        output = self.held_stdout.getvalue()
        self.assertIn("Usage:", output)

    def test_unknown_command(self):
        """Test an unknown command."""
        sys.argv = ['cl.py', 'foobar']
        cl.main()
        output = self.held_stdout.getvalue()
        self.assertIn("Invalid command", output)

    def test_no_command(self):
        """Test with no command provided."""
        sys.argv = ['cl.py']
        cl.main()
        output = self.held_stdout.getvalue()
        self.assertIn("Usage:", output)

if __name__ == '__main__':
    unittest.main()
