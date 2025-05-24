'''Imports to run our tests'''
from app import app
import unittest
from unittest.mock import MagicMock, patch
from ProductionCode import datasource
from datetime import date 

class TestFlaskApp(unittest.TestCase):
    
    @patch('ProductionCode.datasource.DataSource')
    def setUp(self, MockDataSource):
        """Set up the test client for the Flask application."""
        
        self.mock_ds_instance = MagicMock()
        MockDataSource.return_value = self.mock_ds_instance
        self.mock_ds_instance.get_all_countries.return_value = ["USA", "Canada", "Mexico"]
        self.mock_ds_instance.get_sum_between_dates.return_value = (1000, 50) # (total_cases, total_deaths)
        self.mock_ds_instance.get_closest_date.return_value = date(2020, 1, 1) # A sample date
        self.mock_ds_instance.get_sum_specific.return_value = (200, 10)
        self.mock_ds_instance.get_stats.return_value = [
            ("USA", date(2020, 1, 1), 100, 5),
            ("USA", date(2020, 1, 2), 150, 8)
        ]
        self.mock_ds_instance.get_all_data.return_value = [
            {"Country": "USA", "Date_reported": date(2020, 1, 1), "New_cases": 100, "New_deaths": 5}
        ]
        self.mock_ds_instance.get_week_country_and_new_cases.return_value = [(100,)]
        self.mock_ds_instance.get_week_country_and_new_deaths.return_value = [(5,)]
        from app import app
        self.app = app.test_client()
        self.app.testing = True # Enable Flask's testing mode
        
        self.client = app.test_client()

    def test_homepage(self):
        """Test the homepage loads and contains the welcome message."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to my  Application!', response.data)

    def test_compare_valid_data(self):
        """Test the compare route with valid date and country codes."""
        response = self.app.get('/compare/2020-03-01/US,AF')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'COVID-19 data for 2020-03-01:', response.data)

    def test_valid_stats(self):
        """Test if valid country stats load correctly."""
        response = self.app.get('/stats/US/2020-03-01/2021-03-10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'COVID-19 stats for US', response.data)

    def test_compare_invalid_date(self):
        """Test the compare route with an invalid date format."""
        response = self.app.get('/compare/invalid-date/US,AF')
        self.assertNotEqual(response.status_code, 200)
        
    def test_compare_fun_facts(self):
        """Test the funfacts route."""
        response = self.app.get('/funfacts')
        self.assertNotEqual(response.status_code, 200)  
        self.assertIn(b, response.data) 
    
    def setUp(self, MockDataSource):
        """Set up the test client for the Flask application with mocked DataSource.
        
        MockDataSource is the mock for the DataSource *class*.
        We configure what happens when DataSource() is called,
        and then configure the methods of the resulting mock instance.
        """
        # Create a mock instance that will be returned when DataSource() is called.
        self.mock_ds_instance = MagicMock()
        MockDataSource.return_value = self.mock_ds_instance

        # Configure the mock methods of this mock DataSource instance.
        # These are the methods that your Flask app or covid_stats will call on 'ds'.

        # Mock for ds.get_all_countries() which is called on GET requests for /stats and /compare
        self.mock_ds_instance.get_all_countries.return_value = ["USA", "Canada", "Mexico"]

        # Mock for covid_stats.get_cases_and_deaths_stats which calls ds.get_sum_between_dates
        # and ds.get_closest_date.
        # We'll set up specific return values for these in individual tests if needed,
        # but a default is good here.
        self.mock_ds_instance.get_sum_between_dates.return_value = (1000, 50) # (total_cases, total_deaths)
        self.mock_ds_instance.get_closest_date.return_value = date(2020, 1, 1) # A sample date

        # Mock for covid_stats.compare which calls ds.get_sum_specific and ds.get_closest_date
        self.mock_ds_instance.get_sum_specific.return_value = (200, 10) # (cases, deaths for a specific date)
        
        # Other DataSource methods that might be called by covid_stats or directly
        self.mock_ds_instance.get_stats.return_value = [
            ("USA", date(2020, 1, 1), 100, 5),
            ("USA", date(2020, 1, 2), 150, 8)
        ]
        self.mock_ds_instance.get_all_data.return_value = [
            {"Country": "USA", "Date_reported": date(2020, 1, 1), "New_cases": 100, "New_deaths": 5}
        ]
        self.mock_ds_instance.get_week_country_and_new_cases.return_value = [(100,)]
        self.mock_ds_instance.get_week_country_and_new_deaths.return_value = [(5,)]


        # Import the Flask app *after* the DataSource has been mocked.
        # This ensures that when 'app' is loaded, its global 'ds' (from covid_stats)
        # is our mocked instance, not a real database connection.
        from app import app
        self.app = app.test_client()
        self.app.testing = True # Enable Flask's testing mode

    def test_homepage_loads_correctly(self):
        """Test that the homepage loads and contains the welcome message."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Assuming your index.html has this specific welcome message
        self.assertIn(b"Welcome to the COVID-19 Stats App", response.data)
        # Verify that get_all_countries was NOT called on the homepage
        self.mock_ds_instance.get_all_countries.assert_not_called()


    def test_stats_get_request(self):
        """Test the GET request for the /stats page."""
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Stats Page", response.data) # Assuming stats.html has this heading
        # Verify get_all_countries was called to populate the dropdown
        self.mock_ds_instance.get_all_countries.assert_called_once()


    def test_stats_post_request_valid_data(self):
        """Test submitting the stats form with valid data."""
        # Configure specific mock return values for this test scenario
        self.mock_ds_instance.get_sum_between_dates.return_value = (500, 25)
        self.mock_ds_instance.get_closest_date.side_effect = [date(2020, 3, 1), date(2020, 3, 31)] # For start and end

        response = self.app.post('/stats', data={
            'country': 'USA',
            'beginning_date': '2020-03-01', # Matches form field name in app.py
            'ending_date': '2020-03-31'    # Matches form field name in app.py
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Total cases in USA from 2020-03-01 to 2020-03-31: 500", response.data)
        self.assertIn(b"Total deaths in USA from 2020-03-01 to 2020-03-31: 25", response.data)
        
        # Verify that get_sum_between_dates was called with the correct arguments
        # Note: covid_stats.get_cases_and_deaths_stats will call get_closest_date first
        # then get_sum_between_dates.
        # We are patching DataSource directly, so we assert calls on mock_ds_instance.
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-03-01', 'USA', before=False)
        self.mock_ds_instance.get_closest_date.assert_any_call('2020-03-31', 'USA', before=True)
        self.mock_ds_instance.get_sum_between_dates.assert_called_with("USA", date(2020, 3, 1), date(2020, 3, 31))


    def test_stats_post_request_no_data_found(self):
        """Test submitting the stats form when no data is found for the given range."""
        # Mock get_sum_between_dates to return None, None to simulate no data
        self.mock_ds_instance.get_sum_between_dates.return_value = (None, None)
        self.mock_ds_instance.get_closest_date.side_effect = [None, None] # Simulate no closest dates

        response = self.app.post('/stats', data={
            'country': 'NonexistentCountry',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-07'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No data found for NonexistentCountry near the dates you selected.", response.data)
        self.mock_ds_instance.get_sum_between_dates.assert_called_once()


    def test_compare_get_request(self):
        """Test the GET request for the /compare page."""
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Compare Page", response.data) # Assuming compare.html has this heading
        self.mock_ds_instance.get_all_countries.assert_called_once() # Called to populate dropdown


    def test_compare_post_request_valid_data(self):
        """Test submitting the comparison form with valid data."""
        # Mock the behavior for compare, which calls get_sum_specific and get_closest_date for each country
        # For simplicity, we'll configure get_sum_specific to return data for each country in sequence
        self.mock_ds_instance.get_sum_specific.side_effect = [
            (100, 5),  # For USA
            (200, 10)  # For Canada
        ]
        self.mock_ds_instance.get_closest_date.return_value = date(2020, 1, 1)

        response = self.app.post('/compare', data={
            'countries': ['USA', 'Canada'], # Matches form field name 'countries' (list)
            'week': '2020-01-01'           # Matches form field name 'week'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comparison Result", response.data) # Assuming a heading
        self.assertIn(b"USA on 2020-01-01: 100 cases, 5 deaths.", response.data)
        self.assertIn(b"Canada on 2020-01-01: 200 cases, 10 deaths.", response.data)
        
        self.mock_ds_instance.get_sum_specific.assert_any_call("USA", date(2020, 1, 1))
        self.mock_ds_instance.get_sum_specific.assert_any_call("Canada", date(2020, 1, 1))
        self.mock_ds_instance.get_closest_date.assert_called() # Should be called for each country


    def test_help_page_loads_correctly(self):
        """Test that the /help page loads correctly."""
        response = self.app.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Help Page", response.data) # Assuming help.html has this heading


    def test_404_error_handler(self):
        """Test the custom 404 error handler."""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page not found!", response.data)
        self.assertIn(b"is the error.", response.data) # Check for the dynamic error message part
        
        
    
if __name__ == '__main__':
    unittest.main()
    