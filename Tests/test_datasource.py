"""import unittest
# Correct import for MagicMock and patch from unittest.mock
from unittest.mock import MagicMock, patch
from ProductionCode import datasource
from datetime import date # Import date for mocking date objects

"""'''
class TestDataSource(unittest.TestCase):
    """Unit tests for the DataSource module, mocking PostgreSQL interactions."""

    # Apply the patch decorator at the class level.
    # This will replace psycopg2.connect with a MagicMock for all tests in this class.
    # The mock object is passed as the first argument to setUp and each test method.
    @patch('ProductionCode.datasource.psycopg2.connect')
    def setUp(self, mock_connect):
        """Set up the mock database connection and cursor for each test.
        
        The mock_connect argument is automatically provided by the @patch decorator.
        """
        # Configure the mock_connect to return a mock connection object when called.
        # This simulates a successful database connection.
        self.mock_conn = MagicMock()
        mock_connect.return_value = self.mock_conn
        
        # Configure the mock connection to return a mock cursor object when its .cursor() method is called.
        self.mock_cursor = self.mock_conn.cursor.return_value

        # Instantiate DataSource AFTER the mocks are set up.
        # This ensures that when DataSource's __init__ calls self.connect(),
        # it receives the mocked connection.
        self.ds = datasource.DataSource()
'''"""
    def test_get_sum_between_dates(self):
        '''Test the get_sum_between_dates function with expected return values.'''
        # Configure the mock cursor's fetchone to return a specific tuple of (cases, deaths)
        self.mock_cursor.fetchone.return_value = (100, 5) 
        
        # Call the method on the mocked DataSource instance
        result = self.ds.get_sum_between_dates("Afghanistan", "2020-01-01", "2020-01-12")
        
        # Assert that the result matches the mocked return value
        self.assertEqual(result, (100, 5))
        
        # Verify that the cursor's execute method was called with the correct SQL and parameters.
        # unittest.mock.ANY is used for the SQL string as it can be long and dynamic.
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY, ("Afghanistan", "2020-01-01", "2020-01-12"))
        self.mock_cursor.close.assert_called_once() # Verify cursor was closed

    def test_get_sum_specific(self):
        '''Test the get_sum_specific function with expected return values.'''
        self.mock_cursor.fetchone.return_value = (50, 2) # Returns a tuple of (cases, deaths)
        result = self.ds.get_sum_specific("Afghanistan", "2020-01-05")
        self.assertEqual(result, (50, 2))
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY, ("Afghanistan", "2020-01-05"))
        self.mock_cursor.close.assert_called_once()

    # Renamed this test method to avoid duplication and clarify its purpose
    def test_get_closest_date(self):
        '''Test the get_closest_date function with a mocked date return.'''
        # get_closest_date returns a single date object (or None)
        # Mock fetchone to return a tuple containing a datetime.date object
        self.mock_cursor.fetchone.return_value = (date(2020, 1, 1),) 
        
        result = self.ds.get_closest_date("Afghanistan", "2020-01-05")
        self.assertEqual(result, date(2020, 1, 1)) # Compare with a date object
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY, ("Afghanistan", "2020-01-05"))
        self.mock_cursor.close.assert_called_once()
   
    def test_get_week_country_and_new_case(self):
        '''Test get_week_country_and_new_cases with mocked data.'''
        # fetchall returns a list of tuples, even for single columns
        self.mock_cursor.fetchall.return_value = [(10,), (20,), (30,)] 
        result = self.ds.get_week_country_and_new_cases("Afghanistan", "2020-01-05")
        self.assertEqual(result, [(10,), (20,), (30,)])
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY, ("Afghanistan", "2020-01-05"))
        self.mock_cursor.close.assert_called_once()
        
    def test_get_week_country_and_new_deaths(self):
        '''Test get_week_country_and_new_deaths with mocked data.'''
        self.mock_cursor.fetchall.return_value = [(1,), (2,), (3,)] 
        result = self.ds.get_week_country_and_new_deaths("Afghanistan", "2020-01-05")
        self.assertEqual(result, [(1,), (2,), (3,)])
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY, ("Afghanistan", "2020-01-05"))
        self.mock_cursor.close.assert_called_once()
        
    def test_get_all_countries(self):
        '''Test get_all_countries returning a list of country names.'''
        # fetchall returns a list of tuples, each tuple being a row
        self.mock_cursor.fetchall.return_value = [("Afghanistan",), ("Albania",), ("USA",)] 
        result = self.ds.get_all_countries()
        # The method processes fetchall results into a list of strings
        self.assertEqual(result, ["Afghanistan", "Albania", "USA"]) 
        self.mock_cursor.execute.assert_called_with("SELECT DISTINCT country_name FROM countries ORDER BY country_name;")
        self.mock_cursor.close.assert_called_once()

    def test_get_stats(self):
        '''Test get_stats returning a list of detailed stats tuples.'''
        # Mock fetchall to return multiple rows, each as a tuple
        self.mock_cursor.fetchall.return_value = [
            ("US", date(2020, 3, 1), 100, 5),
            ("US", date(2020, 3, 2), 150, 8)
        ]
        result = self.ds.get_stats("US", date(2020, 3, 1), date(2020, 3, 3))
        expected = [
            ("US", date(2020, 3, 1), 100, 5),
            ("US", date(2020, 3, 2), 150, 8)
        ]
        self.assertEqual(result, expected)
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY, ("US", date(2020, 3, 1), date(2020, 3, 3)))
        self.mock_cursor.close.assert_called_once()

    def test_get_all_data(self):
        '''Test get_all_data returning a list of dictionaries.'''
        # Mock fetchall to return multiple rows, each as a tuple
        self.mock_cursor.fetchall.return_value = [
            ("Country1", date(2020, 1, 1), 100, 5),
            ("Country2", date(2020, 1, 2), 200, 10)
        ]
        result = self.ds.get_all_data()
        expected_data = [
            {"Country": "Country1", "Date_reported": date(2020, 1, 1), "New_cases": 100, "New_deaths": 5},
            {"Country": "Country2", "Date_reported": date(2020, 1, 2), "New_cases": 200, "New_deaths": 10}
        ]
        self.assertEqual(result, expected_data)
        self.mock_cursor.execute.assert_called_with(unittest.mock.ANY)
        self.mock_cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()"""
import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from ProductionCode import datasource


@patch('ProductionCode.datasource.psycopg2.connect')
class TestDataSource(unittest.TestCase):
    """Unit tests for the DataSource module, mocking PostgreSQL interactions."""

    def setUp(self):
        """Patch is applied at the class level. This runs before each test."""
        patcher = patch('ProductionCode.datasource.psycopg2.connect')
        self.addCleanup(patcher.stop)
        self.mock_connect = patcher.start()

        # Mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_connect.return_value = self.mock_conn

        # Instantiate the datasource (will use mocked connection)
        self.ds = datasource.DataSource()

    def test_get_sum_between_dates(self):
        self.mock_cursor.fetchone.return_value = (100, 5)
        result = self.ds.get_sum_between_dates("Afghanistan", "2020-01-01", "2020-01-12")
        self.assertEqual(result, (100, 5))

    def test_get_sum_specific(self):
        self.mock_cursor.fetchone.return_value = (50, 2)
        result = self.ds.get_sum_specific("Afghanistan", "2020-01-05")
        self.assertEqual(result, (50, 2))

    def test_get_closest_date_before_true(self):
        self.mock_cursor.fetchone.return_value = (date(2020, 1, 1),)
        result = self.ds.get_closest_date("Afghanistan", "2020-01-05", before=True)
        self.assertEqual(result, date(2020, 1, 1))

    def test_get_closest_date_before_false(self):
        self.mock_cursor.fetchone.return_value = (date(2020, 1, 10),)
        result = self.ds.get_closest_date("Afghanistan", "2020-01-05", before=False)
        self.assertEqual(result, date(2020, 1, 10))

    def test_get_closest_date_none(self):
        self.mock_cursor.fetchone.return_value = (None,)
        result = self.ds.get_closest_date("Afghanistan", "2020-01-05")
        self.assertIsNone(result)

    def test_get_week_country_and_new_cases(self):
        self.mock_cursor.fetchall.return_value = [(10,), (20,), (30,)]
        result = self.ds.get_week_country_and_new_cases("Afghanistan", "2020-01-05")
        self.assertEqual(result, [(10,), (20,), (30,)])

    def test_get_week_country_and_new_deaths(self):
        self.mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]
        result = self.ds.get_week_country_and_new_deaths("Afghanistan", "2020-01-05")
        self.assertEqual(result, [(1,), (2,), (3,)])

    def test_get_all_countries(self):
        self.mock_cursor.fetchall.return_value = [("Afghanistan",), ("USA",)]
        result = self.ds.get_all_countries()
        self.assertEqual(result, ["Afghanistan", "USA"])

    def test_get_stats(self):
        self.mock_cursor.fetchall.return_value = [
            ("Afghanistan", date(2020, 1, 1), 100, 5),
            ("Afghanistan", date(2020, 1, 2), 200, 10)
        ]
        result = self.ds.get_stats("Afghanistan", "2020-01-01", "2020-01-03")
        self.assertEqual(result, [
            ("Afghanistan", date(2020, 1, 1), 100, 5),
            ("Afghanistan", date(2020, 1, 2), 200, 10)
        ])

    def test_get_all_data(self):
        self.mock_cursor.fetchall.return_value = [
            ("Afghanistan", date(2020, 1, 1), 100, 5),
            ("USA", date(2020, 1, 2), 200, 10)
        ]
        result = self.ds.get_all_data()
        expected = [
            {"Country": "Afghanistan", "Date_reported": date(2020, 1, 1), "New_cases": 100, "New_deaths": 5},
            {"Country": "USA", "Date_reported": date(2020, 1, 2), "New_cases": 200, "New_deaths": 10}
        ]
        self.assertEqual(result, expected)

    def test_connection_failure(self):
        """Test that sys.exit is called on connection failure."""
        with patch('ProductionCode.datasource.psycopg2.connect', side_effect=Exception("fail")), \
             patch('sys.exit') as mock_exit:
            datasource.DataSource()
            mock_exit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
