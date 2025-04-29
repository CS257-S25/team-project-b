"""Imports to run our tests"""
import unittest
from io import StringIO
import sys
import cl
from ProductionCode import covid_stats

class TestCovidStats(unittest.TestCase):
    """Class to hold our test functions for our command line"""
    '''def test_highest(self):
        self.assertEqual(covid_stats.highest('2020-01-01'), "data_1_1") '''
        
    def test_stats(self):
        """Test function for the stats function"""
        self.assertEqual(covid_stats.stats('Afghanistan', '2020-01-01', '2020-01-12'), (0, 0))
        
    def test_compare(self):
        """Test function for the compare function"""
        sys.stdout = StringIO()
        covid_stats.compare('Afghanistan,Albania', '2020-01-01'), (0, 0)
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output, "Total cases in Afghanistan during 2020-01-01: 0\nTotal deaths in Albania from 2020-01-01: 0")
        
    def test_compare_usage_statement(self):
        """Test function for the compare function usage statement"""
        self.assertEqual(covid_stats.compare('Afghanistan,Albania', '2019-01-01'), (0, 0))
        
    def test_cl_main_not_enough_args(self):
        """Test function for the command line main function when not enough arguments are provided"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01']
        i = 3
        while i != 0:
            i -= 1
            sys.stdout = StringIO()
            cl.main()
            printed_output = sys.stdout.getvalue()
            self.assertEqual(printed_output, "Usage:\n  python cl.py compare country1,country2 beginning_date ending_date\n  python cl.py stats country beginning_date ending_date\n  python cl.py highest beginning_date ending_date")
            sys.argv.pop()
    
    def test_cl_main_stats(self):
        """Test function for the command line main function when stats are requested"""
        sys.argv = ['cl.py', 'stats', 'Afghanistan', '2020-01-01', '2020-01-12']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output, "Total cases in Afghanistan from 2020-01-01 to 2020-01-12: 0\nTotal deaths in Afghanistan from 2020-01-01 to 2020-01-12: 0")
        
    def test_cl_main_compare(self):
        """Test function for the command line main function when compare is requested"""
        sys.argv = ['cl.py', 'compare', 'Afghanistan,Albania', '2020-01-01']
        sys.stdout = StringIO()
        cl.main()
        printed_output = sys.stdout.getvalue()
        self.assertEqual(printed_output, "")