import unittest
from app import app
from unittest.mock import patch, MagicMock


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

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
        
    
    
    
    @patch('ProductionCode.datasource.DataSource.get_all_countries')
    def test_stats_get(self, mock_get_all_countries):
        mock_get_all_countries.return_value = ["USA", "Canada"]
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select a country:', response.data)
        self.assertIn(b'USA', response.data)
        self.assertIn(b'Canada', response.data)



    @patch('ProductionCode.datasource.DataSource.get_all_countries')
    def test_homepage(self, mock_get_all_countries):
        mock_get_all_countries.return_value = ["USA", "Canada"]
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # You might want to assert the content of the homepage if it's dynamic

    @patch('ProductionCode.datasource.DataSource.get_all_countries')
    def test_stats_get(self, mock_get_all_countries):
        mock_get_all_countries.return_value = ["USA", "Canada"]
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select a country:', response.data)
        self.assertIn(b'USA', response.data)
        self.assertIn(b'Canada', response.data)

    @patch('ProductionCode.datasource.DataSource.get_all_countries')
    @patch('ProductionCode.covid_stats.get_cases_and_deaths_stats')
    def test_stats_post_data_found(self, mock_get_stats, mock_get_all_countries):
        mock_get_all_countries.return_value = ["USA"]
        mock_get_stats.return_value = (1000, 50, "2023-01-05", "2023-01-20")
        response = self.client.post('/stats', data={
            'country': 'USA',
            'beginning_date': '2023-01-01',
            'ending_date': '2023-01-25'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases in USA from 2023-01-05 to 2023-01-20: 1000', response.data)
        self.assertIn(b'Total deaths in USA from 2023-01-05 to 2023-01-20: 50', response.data)
        self.assertIn(b'Showing data from 2023-01-05 to 2023-01-20 (closest available dates).', response.data)

    @patch('ProductionCode.datasource.DataSource.get_all_countries')
    @patch('ProductionCode.covid_stats.get_cases_and_deaths_stats')
    def test_stats_post_no_data(self, mock_get_stats, mock_get_all_countries):
        mock_get_all_countries.return_value = ["Canada"]
        mock_get_stats.return_value = (None, None, None, None)
        response = self.client.post('/stats', data={
            'country': 'Canada',
            'beginning_date': '2023-02-01',
            'ending_date': '2023-02-10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No data found for Canada near the dates you selected.', response.data)

    @patch('ProductionCode.datasource.DataSource.get_all_countries')
    @patch('ProductionCode.covid_stats.get_cases_and_deaths_stats')
    def test_stats_post_exact_dates(self, mock_get_stats, mock_get_all_countries):
        mock_get_all_countries.return_value = ["UK"]
        mock_get_stats.return_value = (500, 20, "2023-03-01", "2023-03-15")
        response = self.client.post('/stats', data={
            'country': 'UK',
            'beginning_date': '2023-03-01',
            'ending_date': '2023-03-15'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases in UK from 2023-03-01 to 2023-03-15: 500', response.data)
        self.assertIn(b'Total deaths in UK from 2023-03-01 to 2023-03-15: 20', response.data)
        self.assertNotIn(b'Showing data from', response.data) # Ensure no note about date adjustment

    
    

if __name__ == '__main__':
    unittest.main()
