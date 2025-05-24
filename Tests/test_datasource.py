import unittest
from ProductionCode import datasource
from unittest import MagicMock, patch

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MagicMock() 
        self.mock_cursor = self.mock_conn.cursor.return_value


    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_sum_between_dates(self, mock_connect):
        '''This is the test for get_sum_between_dates function in our datasource.py file.'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = ("0 deaths and cases")
        ds = datasource.DataSource()
        self.assertEqual(ds.get_sum_between_dates("Afghanistan", "1-5-2020", "1-12-2020"), "0 deaths and cases")
        
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_sum_specific(self, mock_connect):
        '''This is the test for get_sum_between_dates function in our datasource.py file.'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = ("0 deaths and cases")
        ds = datasource.DataSource()
        self.assertEqual(ds.get_sum_specific("Afghanistan", "1-5-2020"), "0 deaths and cases")
        
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_sum_between_dates(self, mock_connect):
        '''This is the test for get_sum_between_dates function in our datasource.py file.'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = ([0, 1, 2, 3])
        ds = datasource.DataSource()
        self.assertEqual(ds.get_closest_date("Afghanistan", "1-5-2020"), 0)
   
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_week_country_and_new_case(self, mock_connect):
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = ("0 deaths and cases")
        ds = datasource.DataSource()
        self.assertEqual(ds.get_week_country_and_new_cases("Afghanistan", "1-5-2020"), "0 deaths and cases")  
        
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_week_country_and_new_deaths(self, mock_connect):
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = ("0 deaths and cases")
        ds = datasource.DataSource()
        self.assertEqual(ds.get_week_country_and_new_deaths("Afghanistan", "1-5-2020"), "0 deaths and cases")  
        
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_all_countries(self, mock_connect):
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = (["Afghanistan", "Albania"])
        ds = datasource.DataSource()
        self.assertEqual(ds.get_all_countries(), "Afghanistan")
        
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_all_countries(self, mock_connect):
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = (["Afghanistan", "Albania"])
        ds = datasource.DataSource()
        self.assertEqual(ds.get_all_countries(), "Afghanistan")
        
    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_get_all_data(self, mock_connect):
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchone.return_value = ([0, 1, 2, 3])
        ds = datasource.DataSource()
        self.assertEqual(ds.get_all_data(), {
                "Country": 0,
                "Date_reported": 1,
                "New_cases": 2,
                "New_deaths": 3})