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
        cursor.execute(f"SELECT New_cases FROM bigTable where Country = {country} AND Date_reported = {date}")
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
    
if __name__ == "__main__":
    ds = DataSource()
    results = ds.get_week_country_and_new_deaths("Afghanistan", "2023-08-06")
    """results = ds.get_specific()"""
    print(results[0])
    ds.connection.close()
