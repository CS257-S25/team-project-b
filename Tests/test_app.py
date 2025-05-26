import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    """Unit tests for Flask application routes and logic."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        """Test the homepage returns a 200 status and HTML content."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.get_data(as_text=True))

    def test_help_page(self):
        """Test the /help route returns a 200 and HTML content."""
        response = self.app.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.get_data(as_text=True))

    def test_404(self):
        """Test that an unknown route returns a 404 error with a proper message."""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', response.get_data(as_text=True))

    @patch('app.DataSource')
    @patch('app.covid_stats.get_cases_and_deaths_stats')
    def test_stats_get_and_post(self, mock_get_stats, mock_ds_class):
        """Test GET and POST behavior for /stats route."""
        # Mock DataSource.get_all_countries
        mock_ds = MagicMock()
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']
        mock_ds_class.return_value = mock_ds

        # GET /stats returns the country list
        get_response = self.app.get('/stats')
        self.assertEqual(get_response.status_code, 200)
        response_text = get_response.get_data(as_text=True)
        self.assertIn('CountryA', response_text)
        self.assertIn('CountryB', response_text)

        # Mock return for successful stats
        mock_get_stats.return_value = (100, 10, '2020-01-01', '2020-01-10')

        # POST /stats with valid data
        post_response = self.app.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-10'
        })
        post_text = post_response.get_data(as_text=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertIn('100', post_text)
        self.assertIn('10', post_text)

        # Mock return for no data
        mock_get_stats.return_value = (None, None, None, None)
        no_data_response = self.app.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-10'
        })
        no_data_text = no_data_response.get_data(as_text=True)
        self.assertEqual(no_data_response.status_code, 200)
        self.asse
