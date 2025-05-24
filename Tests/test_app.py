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
# test_app.py
import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("ProductionCode.datasource.DataSource")
def test_homepage(mock_ds, client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data or b"html" in rv.data

@patch("ProductionCode.datasource.DataSource")
@patch("ProductionCode.covid_stats.get_cases_and_deaths_stats")
def test_stats_post_found(mock_stats, mock_ds, client):
    mock


