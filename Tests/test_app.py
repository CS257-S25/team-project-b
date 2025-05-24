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
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.ds.get_all_countries')
    def test_index_route(self, mock_get_all):
        mock_get_all.return_value = ["Afghanistan"]
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Afghanistan", response.data)

    @patch('app.ds.get_stats')
    def test_get_data(self, mock_get_stats):
        mock_get_stats.return_value = [("Afghanistan", "2020-03-29", 67, 2)]
        response = self.app.get('/data?country=Afghanistan&start_date=2020-03-28&end_date=2020-03-30')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Afghanistan", response.data)

    def test_missing_params(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing parameters", response.data)

if __name__ == '__main__':
    unittest.main()
