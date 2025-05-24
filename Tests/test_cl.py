import unittest
from io import StringIO
import sys
import cl

class TestCL(unittest.TestCase):
    """Tests for the command-line interface in cl.py."""

    def setUp(self):
        """Set up stdout redirection to capture print output."""
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Reset stdout after each test."""
        sys.stdout = self.original_stdout

    def test_compare_command_valid(self):
        """Test the compare command with valid arguments."""
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn('Total cases in', output)

    def test_stats_command_valid(self):
        """Test the stats command with valid arguments."""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn('Total cases in', output)

    def test_compare_command_missing_args(self):
        """Test compare command with missing arguments."""
        sys.argv = ['cl.py', 'compare', 'Afghanistan']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_stats_command_missing_args(self):
        """Test stats command with missing arguments."""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_no_command(self):
        """Test no command provided."""
        sys.argv = ['cl.py']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Usage:", output)

    def test_unknown_command(self):
        """Test an unknown command."""
        sys.argv = ['cl.py', 'foobar']
        cl.main()
        output = self.captured_output.getvalue()
        self.assertIn("Invalid command", output)

if __name__ == '__main__':
    unittest.main()
