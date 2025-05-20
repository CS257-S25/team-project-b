import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Track Global COVID-19 Data', response.data)

    def test_help_page_loads(self):
        response = self.app.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Need Help?', response.data)

    def test_stats_page_get(self):
        """Test GET request for /stats. Should load even if DB fails."""
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Select a country' in response.data or b'Database connection failed' in response.data)

    def test_compare_page_get(self):
        """Test GET request for /compare. Should load even if DB fails."""
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Compare COVID-19 Stats' in response.data or b'Database connection failed' in response.data)

    def test_404_error(self):
        response = self.app.get('/not-a-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)

if __name__ == '__main__':
    unittest.main()
