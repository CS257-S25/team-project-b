import unittest
from app import app

class BasicAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_stats_page(self):
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)

    def test_compare_page(self):
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 200)

    def test_help_page(self):
        response = self.app.get('/help')
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        response = self.app.get('/not-a-real-page')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
