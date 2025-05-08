import unittest
from io import StringIO
import sys
import textwrap
import cl
from ProductionCode import covid_stats


class TestCovidStats(unittest.TestCase):
    """Unit tests for the COVID stats command-line interface"""

    def setUp(self):
        """Redirect stdout before each test"""
        self._stdout = sys.stdout
        self.fake_out = StringIO()
        sys.stdout = self.fake_out

    def tearDown(self):
        """Restore stdout after each test"""
        sys.stdout = self._stdout

    def get_output(self):
        return self.fake_out.getvalue()

    def expected_usage(self):
        return textwrap.dedent("""\
            Usage:
              python cl.py compare country1,country2..country5 date
              python cl.py stats country beginning_date ending_date
              python cl.py highest beginning_date ending_date
        """)

    def expected_stats_output(self):
        return textwrap.dedent("""\
            Total cases in Afghanistan from 2020-01-01 to 2020-01-12: 0!
            Total deaths in Afghanistan from 2020-01-01 to 2020-01-12: 0!
        """)

    def test_stats_function_direct(self):
        """Test stats function return value directly"""
        self.assertEqual(
            covid_stats.stats('Afghanistan', '2020-01-01', '2020-01-12'), (0, 0))

    def test_print_usage(self):
        """Test output of print_usage function"""
        cl.print_usage()
        self.assertEqual(self.get_output(), self.expected_usage())

    def test_handle_compare_invalid_args(self):
        """Test handle_compare with insufficient args"""
        cl.handle_compare('Afghanistan', '2020-01-01')
        self.assertEqual(self.get_output(), self.expected_usage())

    def test_handle_stats_valid(self):
        """Test handle_stats with valid country and date range"""
        cl.handle_stats('Afghanistan', '2020-01-01', '2020-01-12')
        self.assertEqual(self.get_output(), self.expected_stats_output())

    def test_command_extra_argument(self):
        """Test command dispatch with too many arguments"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12', 'extra']
        cl.command(sys.argv[1:])
        self.assertEqual(self.get_output(), self.expected_usage())

    def test_main_missing_args_variants(self):
        """Test main() for various missing or bad args"""
        test_argv_cases = [
            ['cl.py'],
            ['cl.py', 'stats'],
            ['cl.py', 'compare', 'Afghanistan'],
        ]
        for argv in test_argv_cases:
            with self.subTest(argv=argv):
                sys.argv = argv
                cl.main()
                self.assertEqual(self.get_output(), self.expected_usage())
                self.fake_out.truncate(0)
                self.fake_out.seek(0)

    def test_main_stats_valid(self):
        """Test main() with a valid stats command"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        cl.main()
        self.assertEqual(self.get_output(), self.expected_stats_output())

    def test_main_compare_valid(self):
        """Test main() with a valid compare command"""
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        cl.main()
        expected = textwrap.dedent("""\
            Total cases in Afghanistan during 2020-01-01: 0
            Total deaths in Afghanistan from 2020-01-01: 0
            Total cases in Albania during 2020-01-01: 0
            Total deaths in Albania from 2020-01-01: 0

        """)
        self.assertEqual(self.get_output(), expected)
