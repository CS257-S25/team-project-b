"""Unit tests for Flask app routes and logic using mock dependencies."""

import unittest
from unittest.mock import patch
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
    def test_stats_get(self, mock_data_source):
        """Test GET /stats returns page with mocked countries list"""
        mock_ds = mock_data_source.return_value
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']

        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CountryA', response.get_data(as_text=True))

    @patch('app.covid_stats.get_cases_and_deaths_stats')
    @patch('app.DataSource')
    def test_stats_post_valid(self, mock_data_source, mock_stats_func):
        """Test POST /stats with valid country and dates"""
        mock_ds = mock_data_source.return_value
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
    def test_stats_post_no_data(self, mock_data_source, mock_stats_func):
        """Test POST /stats when no data is returned"""
        mock_ds = mock_data_source.return_value
        mock_ds.get_all_countries.return_value = ['CountryA']
        mock_stats_func.return_value = (None, None, None, None)

        response = self.client.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-02'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!doc', response.get_data(as_text=True))

    @patch('app.covid_stats.compare')
    @patch('app.DataSource')
    def test_compare_post(self, mock_data_source, mock_compare_func):
        """Test POST /compare with valid countries and week"""
        mock_ds = mock_data_source.return_value
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
    def test_compare_get(self, mock_data_source):
        """Test GET /compare returns countries list"""
        mock_ds = mock_data_source.return_value
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']

        response = self.client.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CountryA', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
