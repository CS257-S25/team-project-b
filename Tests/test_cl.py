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
import sys
from ProductionCode import cl

class TestCL(unittest.TestCase):
    def setUp(self):
        patcher = patch('ProductionCode.cl.DataSource')
        self.mock_ds_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_ds = self.mock_ds_class.return_value

    def test_main_summary_command_success(self):
        args = ['cl.py', 'summary', 'USA', '2021-01-01', '2021-01-10']
        with patch.object(sys, 'argv', args):
            self.mock_ds.get_sum_between_dates.return_value = (1000, 50)
            try:
                cl.main()
            except SystemExit:
                self.fail("main() exited unexpectedly on valid args")

    def test_main_summary_command_no_data(self):
        args = ['cl.py', 'summary', 'USA', '2021-01-01', '2021-01-10']
        with patch.object(sys, 'argv', args):
            self.mock_ds.get_sum_between_dates.return_value = (None, None)
            try:
                cl.main()
            except SystemExit:
                self.fail("main() exited unexpectedly when no data")

    def test_main_invalid_command(self):
        args = ['cl.py', 'invalidcmd']
        with patch.object(sys, 'argv', args):
            with self.assertRaises(SystemExit):
                cl.main()

    def test_main_missing_arguments(self):
        args = ['cl.py']
        with patch.object(sys, 'argv', args):
            with self.assertRaises(SystemExit):
                cl.main()

if __name__ == '__main__':
    unittest.main()
