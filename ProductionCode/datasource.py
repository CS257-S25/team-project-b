'''Module to handle passwords for database connection'''
import sys
import psycopg2
import ProductionCode.psqlConfig as config

class DataSource:
    """Class to handle database connection and queries for covid data."""

    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.'''

        try:
            self.connection = psycopg2.connect(database=config.database,
                                user=config.user, password=config.password, host="localhost")
        except psycopg2.OperationalError as e:
            sys.exit(f"""Unable to connect to the database. Error was {e}.
                     Please check your connection settings.""")
        return self.connection


    def get_sum_between_dates(self, country, start_date, end_date):
        '''Returns the sum of new cases and new deaths for a specific country
           between a given start and end date.'''
        cursor = self.connection.cursor()
        # Adjusted query to join covid_data with countries and dates tables
        # and use correct column names (cases, deaths, country_name, report_date).
        cursor.execute("""
            SELECT 
                SUM(cd.cases), 
                SUM(cd.deaths) 
            FROM 
                covid_data AS cd
            JOIN 
                countries AS c ON cd.country_id = c.id
            JOIN 
                dates AS d ON cd.date_id = d.id
            WHERE 
                c.country_name = %s 
                AND d.report_date BETWEEN %s AND %s
        """, (country, start_date, end_date,))
        results_to_return = cursor.fetchone()
        cursor.close()
        return results_to_return

    def get_sum_specific(self, country, date): # Renamed 'week' parameter to 'date' for clarity
        '''Returns the sum of new cases and new deaths for a specific country
           on a specific date.'''
        cursor = self.connection.cursor()
        # Adjusted query to join covid_data with countries and dates tables
        # and use correct column names (cases, deaths, country_name, report_date).
        cursor.execute("""
            SELECT 
                SUM(cd.cases), 
                SUM(cd.deaths) 
            FROM 
                covid_data AS cd
            JOIN 
                countries AS c ON cd.country_id = c.id
            JOIN 
                dates AS d ON cd.date_id = d.id
            WHERE 
                c.country_name = %s 
                AND d.report_date = %s
        """, (country, date,)) # Using 'date' parameter
        results_returning = cursor.fetchone()
        cursor.close()
        return results_returning

    def get_closest_date(self, target_date, country, before=True):
        """Get the closest available date for the country."""
        try:
            cursor = self.connection.cursor()
            if before:
                query = """
                    SELECT MAX(d.report_date) 
                    FROM covid_data AS cd
                    JOIN countries AS c ON cd.country_id = c.id
                    JOIN dates AS d ON cd.date_id = d.id
                    WHERE c.country_name = %s AND d.report_date <= %s;
                """
            else:
                query = """
                    SELECT MIN(d.report_date) 
                    FROM covid_data AS cd
                    JOIN countries AS c ON cd.country_id = c.id
                    JOIN dates AS d ON cd.date_id = d.id
                    WHERE c.country_name = %s AND d.report_date >= %s;
                """
            cursor.execute(query, (country, target_date))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result and result[0] else None

        except psycopg2.OperationalError as e:
            print("Error finding closest date:", e)
            return None

    def get_week_country_and_new_cases(self, country, date):
        '''Returns the new cases for a specific country on a specific date.'''
        cursor = self.connection.cursor()
        # Adjusted query to join covid_data with countries and dates tables
        # and use correct column names (cases, country_name, report_date).
        cursor.execute("""
            SELECT 
                cd.cases 
            FROM 
                covid_data AS cd
            JOIN 
                countries AS c ON cd.country_id = c.id
            JOIN 
                dates AS d ON cd.date_id = d.id
            WHERE 
                c.country_name = %s 
                AND d.report_date = %s
        """, (country, date,))
        result_to_return = cursor.fetchall()
        cursor.close() # Added cursor.close()
        return result_to_return

    def get_week_country_and_new_deaths(self, country, date):
        '''Returns the new deaths for a specific country on a specific date.'''
        cursor = self.connection.cursor()
        # Adjusted query to join covid_data with countries and dates tables
        # and use correct column names (deaths, country_name, report_date).
        cursor.execute("""
            SELECT 
                cd.deaths 
            FROM 
                covid_data AS cd
            JOIN 
                countries AS c ON cd.country_id = c.id
            JOIN 
                dates AS d ON cd.date_id = d.id
            WHERE 
                c.country_name = %s 
                AND d.report_date = %s
        """, (country, date,))
        results_we_are_returning = cursor.fetchall()
        cursor.close() # Added cursor.close()
        return results_we_are_returning

    def get_all_countries(self):
        '''Returns a list of all country names from the countries table.'''
        cursor = self.connection.cursor()
        # Adjusted query to select from the countries table directly
        cursor.execute("SELECT DISTINCT country_name FROM countries ORDER BY country_name;")
        countries = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return countries

    def get_stats(self, country, beginning_date, ending_date):
        '''Gets the covid stats (country name, report date, cases, deaths)
           for a specific country within a date range.'''
        cursor = self.connection.cursor()
        # Adjusted query to join covid_data with countries and dates tables
        # and select specific columns.
        cursor.execute("""
            SELECT 
                c.country_name, 
                d.report_date, 
                cd.cases, 
                cd.deaths 
            FROM 
                covid_data AS cd
            JOIN 
                countries AS c ON cd.country_id = c.id
            JOIN 
                dates AS d ON cd.date_id = d.id
            WHERE 
                c.country_name = %s 
                AND d.report_date > %s 
                AND d.report_date < %s
        """, (country, beginning_date, ending_date))

        # Directly return the fetched results as a list of tuples.
        # The previous Python loop was redundant as fetchall() already returns
        # data in a suitable format (list of tuples).
        value = cursor.fetchall()
        cursor.close()
        return value


    def get_all_data(self):
        '''Returns all rows from the covid_data table along with country name and report date.'''
        cursor = self.connection.cursor()
        # Adjusted query to join covid_data with countries and dates tables
        # and select specific columns.
        cursor.execute("""
            SELECT 
                c.country_name, 
                d.report_date, 
                cd.cases, 
                cd.deaths 
            FROM 
                covid_data AS cd
            JOIN 
                countries AS c ON cd.country_id = c.id
            JOIN 
                dates AS d ON cd.date_id = d.id
        """)
        rows = cursor.fetchall()
        cursor.close()

        # Convert results to list of dictionaries for easier use
        data = []
        for row in rows:
            data.append({
                "Country": row[0],
                "Date_reported": row[1],
                "New_cases": row[2],
                "New_deaths": row[3]
            })
        return data

if __name__ == "__main__":
    ds = DataSource()
    results = ds.get_stats("Afghanistan", "2023-06-18", "20203-08-06")
    cases_results = ds.get_week_country_and_new_cases("Afghanistan", "2023-08-06")
    """results = ds.get_specific()"""
    for i in results:
        print(i)
    print(cases_results[0][0])
    ds.connection.close()
