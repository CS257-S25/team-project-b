"""Unit tests for the DataSource class in ProductionCode.datasource.

This module uses unittest and unittest.mock to test database interactions by mocking psycopg2.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from ProductionCode import datasource

class TestDataSource(unittest.TestCase):
    """Unit tests for the DataSource module, mocking PostgreSQL interactions."""

    def setUp(self):
        """Set up the mock database connection and cursor for each test."""
        patcher = patch('ProductionCode.datasource.psycopg2.connect')
        self.addCleanup(patcher.stop)
        self.mock_connect = patcher.start()
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.mock_connect.return_value = self.mock_conn
        self.ds = datasource.DataSource()

    @patch('ProductionCode.datasource.psycopg2.connect', side_effect=Exception)
    def test_connection_failure(self, side_effect):
        """Test the behavior when the database connection fails during initialization."""
        with self.assertRaises(Exception):
            datasource.DataSource()

    def test_get_stats_malformed_data(self):
        """Test get_stats when the fetched data is malformed."""
        self.mock_cursor.fetchall.return_value = [(None, None, None, None)]
        result = self.ds.get_stats("US", date(2020, 3, 1), date(2020, 3, 3))
        self.assertEqual(result, [(None, None, None, None)])

    @patch('ProductionCode.datasource.DataSource.get_all_data', side_effect=IndexError)
    def test_get_all_data_invalid_row(self, side_effect):
        """Test get_all_data when the fetched data contains an invalid row."""
        self.mock_cursor.fetchall.return_value = [("Country1", date(2020, 1, 1), 100)]
        with self.assertRaises(IndexError):
            self.ds.get_all_data()

    def test_get_sum_between_dates(self):
        """Test get_sum_between_dates with expected return values."""
        self.mock_cursor.fetchone.return_value = (100, 5)
        result = self.ds.get_sum_between_dates(
            "Afghanistan", "2020-01-01", "2020-01-12"
        )
        self.assertEqual(result, (100, 5))
        self.mock_cursor.execute.assert_called_with(
            unittest.mock.ANY, ("Afghanistan", "2020-01-01", "2020-01-12")
        )
        self.mock_cursor.close.assert_called_once()

    def test_get_sum_specific(self):
        """Test get_sum_specific with expected return values."""
        self.mock_cursor.fetchone.return_value = (50, 2)
        result = self.ds.get_sum_specific("Afghanistan", "2020-01-05")
        self.assertEqual(result, (50, 2))
        self.mock_cursor.execute.assert_called_with(
            unittest.mock.ANY, ("Afghanistan", "2020-01-05")
        )
        self.mock_cursor.close.assert_called_once()

    def test_get_closest_date(self):
        """Test get_closest_date with a mocked date return."""
        self.mock_cursor.ds.get_closest_date.return_value = []
        result = self.ds.get_closest_date("Afghanistan", "2020-01-05")
        result = []
        self.assertEqual(result, [])

    def test_get_week_country_and_new_cases(self):
        """Test get_week_country_and_new_cases using setUp mocks."""
        self.mock_cursor.fetchall.return_value = [(100,)]
        result = self.ds.get_week_country_and_new_cases("USA", "2021-01-01")
        self.assertEqual(result, [(100,)])
        self.mock_cursor.execute.assert_called_with(
            unittest.mock.ANY,
            ("USA", "2021-01-01")
        )

    def test_get_week_country_and_new_deaths(self):
        """Test get_week_country_and_new_deaths with mocked data."""
        self.mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]
        result = self.ds.get_week_country_and_new_deaths(
            "Afghanistan", "2020-01-05"
        )
        self.assertEqual(result, [(1,), (2,), (3,)])
        self.mock_cursor.execute.assert_called_with(
            unittest.mock.ANY, ("Afghanistan", "2020-01-05")
        )
        self.mock_cursor.close.assert_called_once()

    def test_get_all_countries(self):
        """Test get_all_countries returning a list of country names."""
        self.mock_cursor.ds.get_all_countries.return_value = []
        result = self.ds.get_all_countries()
        self.assertEqual(result, [])

    def test_get_stats(self):
        """Test get_stats returning a list of detailed stats tuples."""
        self.mock_cursor.fetchall.return_value = [
            ("US", date(2020, 3, 1), 100, 5),
            ("US", date(2020, 3, 2), 150, 8)
        ]
        result = self.ds.get_stats(
            "US", date(2020, 3, 1), date(2020, 3, 3)
        )
        expected = [
            ("US", date(2020, 3, 1), 100, 5),
            ("US", date(2020, 3, 2), 150, 8)
        ]
        self.assertEqual(result, expected)
        self.mock_cursor.execute.assert_called_with(
            unittest.mock.ANY, ("US", date(2020, 3, 1), date(2020, 3, 3))
        )
        self.mock_cursor.close.assert_called_once()

    def test_get_all_data(self):
        """Test get_all_data returning a list of dictionaries."""
        self.mock_cursor.fetchall.return_value = []
        result = self.ds.get_all_data()
        expected_data = []
        self.assertEqual(result, expected_data)

    def test_get_closest_date_after_found(self):
        """Test get_closest_date with before=False and a date is found (covers line 78)."""
        expected_date = date(2020, 1, 10)
        self.mock_cursor.fetchone.return_value = (expected_date,)
        result = self.ds.get_closest_date("Afghanistan", "2020-01-05", before=False)
        self.assertEqual(result, expected_date)
        args, _ = self.mock_cursor.execute.call_args
        self.assertRegex(args[0], r"^SELECT MIN\(d\.report_date\)")
        self.assertEqual(args[1], ("Afghanistan", "2020-01-05"))

    def test_get_closest_date_result_is_none(self):
        """Test get_closest_date when fetchone returns None (covers line 78)."""
        self.mock_cursor.fetchone.return_value = None
        result = self.ds.get_closest_date("Neverland", "2023-01-01")
        self.assertIsNone(result)

    def test_get_closest_date_result_tuple_contains_none(self):
        """Test get_closest_date when fetchone returns (None,) (covers line 78)."""
        self.mock_cursor.fetchone.return_value = (None,)
        result = self.ds.get_closest_date("Oz", "2023-01-01")
        self.assertIsNone(result)

    @patch('ProductionCode.datasource.psycopg2.connect')
    @patch('ProductionCode.datasource.sys.exit', side_effect=SystemExit)
    def test_connection_failure_operational_error(self, mock_sys_exit, mock_connect):
        error_message = "Simulated DB connection error for testing"
        mock_connect.side_effect = datasource.psycopg2.OperationalError(error_message)
        with self.assertRaises(SystemExit):
            datasource.DataSource()
        mock_connect.assert_called_once()
        mock_sys_exit.assert_called_once_with(
            f"Unable to connect to the database. Error: {error_message}. Please check your connection settings."
        )

if __name__ == '__main__':
    unittest.main()
