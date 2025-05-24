import unittest
from unittest.mock import patch, MagicMock
import cl
from ProductionCode import covid_stats

class TestCL(unittest.TestCase):
    def setUp(self):
        patcher = patch('ProductionCode.covid_stats.DataSource')
        self.addCleanup(patcher.stop)
        self.mock_ds_class = patcher.start()
        self.mock_ds = MagicMock()
        self.mock_ds_class.return_value = self.mock_ds

        self.mock_ds.get_all_data.return_value = [
            {"Country": "Afghanistan", "Date_reported": date(2020, 1, 1), "New_cases": 10, "New_deaths": 1}
        ]
        self.mock_ds.get_sum_between_dates.return_value = (10, 1)
        self.mock_ds.get_sum_specific.return_value = (5, 0)

    def test_compare_command_valid(self):
        with patch('sys.argv', ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']):
            cl.main()

    def test_stats_command_valid(self):
        with patch('sys.argv', ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-10']):
            cl.main()

    def test_print_usage(self):
        with patch('sys.argv', ['cl.py']):
            cl.main()

    def test_invalid_command(self):
        with patch('sys.argv', ['cl.py', 'foobar']):
            cl.main()

if __name__ == '__main__':
    unittest.main()
