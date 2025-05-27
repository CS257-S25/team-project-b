'''import unittest
from app import app, DataSource
import os
from unittest.mock import patch

class TestApp(unittest.TestCase):
    """Unit tests for Flask application routes and logic."""

    def setUp(self):
        """Setup the test client and prepare test environment."""
        self.app = app.test_client()
        self.app.testing = True

        # Optional: Set up a test CSV if your DataSource reads from it
        self.test_data_path = "data/countries-aggregated.csv"
        if not os.path.exists(self.test_data_path):
            os.makedirs("data", exist_ok=True)
            with open(self.test_data_path, "w") as f:
                f.write("Date,Country,Confirmed,Deaths,Recovered\n")
                f.write("2020-01-01,CountryA,10,1,0\n")
                f.write("2020-01-02,CountryA,15,2,0\n")
                f.write("2020-01-01,CountryB,20,1,0\n")
                f.write("2020-01-02,CountryB,25,3,0\n")

    def test_homepage(self):
        """Test the homepage route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.get_data(as_text=True))

    def test_help_page(self):
        """Test the help page route."""
        response = self.app.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.get_data(as_text=True))

    def test_404(self):
        """Test non-existent page returns 404."""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', response.get_data(as_text=True))

    def test_stats_get(self):
        """Test GET request to /stats shows available countries."""
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CountryA', response.get_data(as_text=True))

    def test_stats_post_valid(self):
        """Test POST request to /stats with valid input."""
        response = self.app.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-02'
        })
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Total cases', html)
        self.assertIn('Total deaths', html)
        self.assertIn('15', html)  # Confirmed on 2020-01-02
        self.assertIn('2', html)   # Deaths on 2020-01-02

    """" vvv THIS IS NEW, MIGHT DELETE vvv """
#Helper function for the tests
    def post_stats(self, country, beginning_date, ending_date):
        return self.app.post('/stats', data={
            'country': country,
            'beginning_date': beginning_date,
            'ending_date': ending_date
        })

    def post_compare(self, countries, week):
        return self.app.post('/compare', data={
            'countries': countries,
            'week': week
        })

    @patch('app.covid_stats.get_cases_and_deaths_stats')
    @patch('app.DataSource')
    def test_stats_post_invalid_data(self, mock_ds, mock_get_stats):
        mock_ds.return_value.get_all_countries.return_value = ['FakeCountry']
        mock_get_stats.return_value = (None, None, None, None)  # Simulate no data
        response = self.post_stats('FakeCountry', '2020-01-01', '2020-01-02')
        self.assertEqual(response.status_code, 200)
        self.assertIn('No data found for FakeCountry', response.get_data(as_text=True))

    @patch('app.covid_stats.get_cases_and_deaths_stats')
    @patch('app.DataSource')
    def test_stats_post_with_note_about_dates(self, mock_ds, mock_get_stats):
        mock_ds.return_value.get_all_countries.return_value = ['CountryA']
        mock_get_stats.return_value = (100, 10, '2020-01-02', '2020-01-05')  # Different from request

        response = self.post_stats('CountryA', '2020-01-01', '2020-01-10')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Showing data from 2020-01-02 to 2020-01-05', html)
        self.assertIn('100', html)
        self.assertIn('10', html)

    @patch('app.covid_stats.compare')
    @patch('app.DataSource')
    def test_compare_post_with_mock_data(self, mock_ds, mock_compare):
        mock_ds.return_value.get_all_countries.return_value = ['CountryA', 'CountryB']
        mock_compare.return_value = (
            {'CountryA': {'cases': 100}, 'CountryB': {'cases': 200}},
            {'labels': ['Mon', 'Tue'], 'data': [50, 100]}
        )

        response = self.post_compare(['CountryA', 'CountryB'], '2020-W01')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('CountryA', html)
        self.assertIn('CountryB', html)
        self.assertIn('100', html)

    """ ^^^ THIS IS NEW, MIGHT DELETE ^^^ """

    def test_compare_get(self):
        """Test GET request to /compare returns countries."""
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CountryA', response.get_data(as_text=True))

    def test_compare_post(self):
        """Test POST to /compare with valid countries and week."""
        response = self.app.post('/compare', data={
            'countries': ['CountryA', 'CountryB'],
            'week': '2020-W01'
        })
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('CountryA', html)
        self.assertIn('CountryB', html)
        self.assertIn('Total cases', html)

if __name__ == '__main__':
    unittest.main()'''
import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    """Unit tests for Flask application routes and logic using mocks."""

    def setUp(self):
        """Create test client for the app."""
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage(self):
        """Test GET /"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.get_data(as_text=True))

    def test_help_page(self):
        """Test GET /help"""
        response = self.client.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.get_data(as_text=True))

    def test_404_page(self):
        """Test GET to an invalid route returns 404"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', response.get_data(as_text=True))

    @patch('app.DataSource')
    def test_stats_get(self, MockDataSource):
        """Test GET /stats returns page with mocked countries list"""
        mock_ds = MockDataSource.return_value
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']
        
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CountryA', response.get_data(as_text=True))

    @patch('app.covid_stats.get_cases_and_deaths_stats')
    @patch('app.DataSource')
    def test_stats_post_valid(self, MockDataSource, mock_stats_func):
        """Test POST /stats with valid country and dates"""
        mock_ds = MockDataSource.return_value
        mock_ds.get_all_countries.return_value = ['CountryA']
        mock_stats_func.return_value = (100, 5, '2020-01-01', '2020-01-02')

        response = self.client.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-02'
        })

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('100', html)
        self.assertIn('5', html)
        self.assertIn('2020-01-01', html)
        self.assertIn('2020-01-02', html)

    @patch('app.covid_stats.get_cases_and_deaths_stats')
    @patch('app.DataSource')
    def test_stats_post_no_data(self, MockDataSource, mock_stats_func):
        """Test POST /stats when no data is returned"""
        mock_ds = MockDataSource.return_value
        mock_ds.get_all_countries.return_value = ['CountryA']
        mock_stats_func.return_value = (None, None, None, None)

        response = self.client.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-02'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('No data found for CountryA', response.get_data(as_text=True))

    @patch('app.covid_stats.compare')
    @patch('app.DataSource')
    def test_compare_post(self, MockDataSource, mock_compare_func):
        """Test POST /compare with valid countries and week"""
        mock_ds = MockDataSource.return_value
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']
        mock_compare_func.return_value = (
            "Comparison results",
            {"labels": ["CountryA"], "cases": [100], "deaths": [5]}
        )

        response = self.client.post('/compare', data={
            'countries': ['CountryA'],
            'week': '2020-01-01'
        })

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Comparison results', html)
        self.assertIn('CountryA', html)
        self.assertIn('100', html)
        self.assertIn('5', html)

    @patch('app.DataSource')
    def test_compare_get(self, MockDataSource):
        """Test GET /compare returns countries list"""
        mock_ds = MockDataSource.return_value
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']

        response = self.client.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CountryA', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
