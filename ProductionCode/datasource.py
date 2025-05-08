import psycopg2
import psql_Config as config

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

    def get_week_country_and_new_cases(self, country, date):
        '''Returns the week, country and the number of new cases.'''
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT New_cases FROM bigTable where Country =%s AND Date_reported =%s", (country, date,))
        results = cursor.fetchall()
        return results
    
    def get_week_country_and_new_deaths(self, country, date):
        '''Returns the week, country and the number of new cases.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT New_deaths FROM bigTable where Country =%s AND Date_reported =%s", (country, date,))
        results = cursor.fetchall()
        return results
    
    def get_specific(self):
        '''Returns the values of Afghanistan in the table.'''
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bigTable WHERE Country =%s", ('Afghanistan',))
        value = cursor.fetchall()
        return value
    
    def get_stats(self, country, beginning_date, ending_date):
        '''bruh'''
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
