import psycopg2
from . import psql_Config as config

class DataSource:

    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.'''

        try:
            self.connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return self.connection
    
    
    def get_sum_between_dates(self, country, start_date, end_date):
        '''Returns the week, country and the number of new cases.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(New_cases), SUM(New_deaths) FROM bigTable WHERE Country = %s AND Date_reported BETWEEN %s AND %s", (country, start_date, end_date,))
        results = cursor.fetchone()
        cursor.close()
        return results

    def get_sum_specific(self, country, week):
        '''Returns the week, country and the number of new cases.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(New_cases), SUM(New_deaths) FROM bigTable WHERE Country = %s AND Date_reported = %s", (country, week,))
        results = cursor.fetchone()
        cursor.close()
        return results

    def get_closest_date(self, target_date, country, before=True):
        """Get the closest available date for the country."""
        try:
            cursor = self.connection.cursor()
            if before:
                query = """
                    SELECT MAX(Date_reported) FROM bigTable
                    WHERE Country = %s AND Date_reported <= %s;
                """
            else:
                query = """
                    SELECT MIN(Date_reported) FROM bigTable
                    WHERE Country = %s AND Date_reported >= %s;
                """
            cursor.execute(query, (country, target_date))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result and result[0] else None
        except Exception as e:
            print("Error finding closest date:", e)
            return None
    
    def get_week_country_and_new_cases(self, country, date):
        '''Returns the week, country and the number of new cases.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT New_cases FROM bigTable where Country =%s AND Date_reported =%s", (country, date,))
        results = cursor.fetchall()
        return results
    
    def get_week_country_and_new_deaths(self, country, date):
        '''Returns the week, country and the number of new cases.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT New_deaths FROM bigTable where Country =%s AND Date_reported =%s", (country, date,))
        results = cursor.fetchall()
        return results
    
    def get_all_countries(self):
        '''Returns a list of all country names from the bigTable.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT Country FROM bigTable ORDER BY Country;")
        countries = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return countries
    
    def get_stats(self, country, beginning_date, ending_date):
        '''Gets the covid stats for a specific country at a date range'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bigTable WHERE Country =%s AND Date_reported >%s AND Date_reported <%s", (country, beginning_date, ending_date))
        value = cursor.fetchall()
        i = 0
        length = len(value)
        results_list = []
        while i < length:
            j = 0
            small_list = []
            while j < 5:
                small_list.append(results[i][j])
                j += 1
            results_list.append(small_list)
            i += 1
        return results_list
    
if __name__ == "__main__":
    ds = DataSource()
    results = ds.get_stats("Afghanistan", "2023-06-18", "20203-08-06")
    cases_results = ds.get_week_country_and_new_cases("Afghanistan", "2023-08-06")
    """results = ds.get_specific()"""
    for i in results:
        print(i)
    print(cases_results[0][0])
    ds.connection.close()
