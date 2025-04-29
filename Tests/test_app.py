import unittest
from io import StringIO
import sys
import app

class TestCovidStats(unittest.TestCase):
    """Test file for our flask app"""
    def test_about_page(self):
        self.assertEqual(app.aboutpage(), "Hello, this is the about page.")
        
    def test_cl_main_not_enough_args(self):
        pass