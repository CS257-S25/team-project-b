import unittest
from app import app, DataSource
import os

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

    def test_stats_post_invalid_country(self):
        """Test POST to /stats with a fake country."""
        response = self.app.post('/stats', data={
            'country': 'FakeCountry',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('No data found', response.get_data(as_text=True))

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
    unittest.main()
