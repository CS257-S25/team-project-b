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
from ProductionCode import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.client = app.app.test_client()

        # Patch DataSource in app.py
        patcher = patch('ProductionCode.app.DataSource')
        self.mock_ds_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_ds = self.mock_ds_class.return_value

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter a country and date range', response.data)

    def test_results_route_success(self):
        # Mock DB method to return sample data
        self.mock_ds.get_sum_between_dates.return_value = (1234, 56)
        response = self.client.post('/results', data={
            'country': 'USA',
            'start_date': '2021-01-01',
            'end_date': '2021-01-10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'COVID-19 Summary for USA', response.data)
        self.mock_ds.get_sum_between_dates.assert_called_once_with('USA', '2021-01-01', '2021-01-10')

    def test_results_route_missing_fields(self):
        # Missing country and end_date
        response = self.client.post('/results', data={
            'country': '',
            'start_date': '2021-01-01',
            'end_date': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing data', response.data)

    def test_results_route_no_data(self):
        # Simulate no data returned (None)
        self.mock_ds.get_sum_between_dates.return_value = (None, None)
        response = self.client.post('/results', data={
            'country': 'USA',
            'start_date': '2021-01-01',
            'end_date': '2021-01-10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases: 0', response.data)
        self.assertIn(b'Total deaths: 0', response.data)

    def test_404_error(self):
        response = self.client.get('/not_a_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 Not Found', response.data)

if __name__ == '__main__':
    unittest.main()

