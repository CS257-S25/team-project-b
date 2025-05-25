"""import unittest
from app import app
from unittest.mock import patch, MagicMock

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_submit_post(self):
        response = self.client.post('/stats', data={'country': 'Afghanistan', 'beginning_date': '2020-01-01', 'ending_date': '2020-01-12'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!doctype', response.data)  

    def test_submit_post(self):
        response = self.client.post('/stats', data={'country': 'Afghanistan', 'beginning_date': '2022-01-01', 'ending_date': '2022-01-12'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!doctype', response.data)  

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_stats_get(self):
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_stats_post_valid(self):
        response = self.client.post('/stats', data={
            'country': 'Afghanistan',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases', response.data)

    def test_stats_post_invalid(self):
        response = self.client.post('/stats', data={
            'country': 'FakeCountry',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No data found', response.data)

    def test_compare_get(self):
        response = self.client.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_compare_post(self):
        response = self.client.post('/compare', data={
            'countries': ['Afghanistan', 'Albania'],
            'week': '2020-01-01'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases', response.data)

    def test_help_page(self):
        response = self.client.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_404_page(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)

if __name__ == '__main__':
    unittest.main()"""
import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_help_page(self):
        response = self.client.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_404_page(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)

    @patch('app.DataSource')
    @patch('app.covid_stats.get_cases_and_deaths_stats')
    def test_stats_get_and_post(self, mock_get_stats, mock_ds_class):
        mock_ds = MagicMock()
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']
        mock_ds_class.return_value = mock_ds

        # GET request
        get_response = self.client.get('/stats')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(b'CountryA', get_response.data)

        # POST request with valid data
        mock_get_stats.return_value = (100, 20, '2020-01-01', '2020-01-10')
        post_response = self.client.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-10'
        })
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'100', post_response.data)
        self.assertIn(b'20', post_response.data)

        # POST with adjusted dates note
        mock_get_stats.return_value = (50, 5, '2020-01-02', '2020-01-09')
        adjusted_response = self.client.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-10'
        })
        self.assertIn(b'Showing data from 2020-01-02 to 2020-01-09', adjusted_response.data)

        # POST with no data
        mock_get_stats.return_value = (None, None, None, None)
        no_data_response = self.client.post('/stats', data={
            'country': 'CountryA',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-10'
        })
        self.assertIn(b'No data found', no_data_response.data)

    @patch('app.DataSource')
    @patch('app.covid_stats.compare')
    def test_compare_get_and_post(self, mock_compare, mock_ds_class):
        mock_ds = MagicMock()
        mock_ds.get_all_countries.return_value = ['CountryA', 'CountryB']
        mock_ds_class.return_value = mock_ds

        # GET request
        get_response = self.client.get('/compare')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(b'CountryA', get_response.data)

        # POST request
        mock_compare.return_value = ({'CountryA': 100, 'CountryB': 50}, {'chart': 'data'})
        post_response = self.client.post('/compare', data={
            'countries': ['CountryA', 'CountryB'],
            'week': '2020-W01'
        })
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b'CountryA', post_response.data)
        self.assertIn(b'CountryB', post_response.data)

if __name__ == '__main__':
    unittest.main()
