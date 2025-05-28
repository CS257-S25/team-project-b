import psycopg2
from . import psql_Config as config

class DataSource:
    """Manages database connection and queries for COVID-19 data."""

    def __init__(self):
        """Constructor that initiates connection to database."""
        self.connection = self.connect()

    def connect(self):
        """Connect to the database using psql_Config."""
        try:
            return psycopg2.connect(
                database=config.database,
                user=config.user,
                password=config.password,
                host="localhost"
            )
        except Exception as e:
            print("Connection error:", e)
            exit()

    def get_sum_between_dates(self, country, start_date, end_date):
        """Returns total cases and deaths for a country between two dates."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT SUM(New_cases), SUM(New_deaths)
            FROM bigTable
            WHERE Country = %s AND Date_reported BETWEEN %s AND %s
        """, (country, start_date, end_date))
        results = cursor.fetchone()
        cursor.close()
        return results

    def get_sum_specific(self, country, week):
        """Returns total cases and deaths for a country on a specific date."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT SUM(New_cases), SUM(New_deaths)
            FROM bigTable
            WHERE Country = %s AND Date_reported = %s
        """, (country, week))
        results = cursor.fetchone()
        cursor.close()
        return results

    def get_closest_date(self, target_date, country, before=True):
        """Get the closest available date for the country."""
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

    def get_week_country_and_new_cases(self, country, date):
        """Get new cases for a specific country on a specific date."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT New_cases FROM bigTable
            WHERE Country = %s AND Date_reported = %s
        """, (country, date))
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_week_country_and_new_deaths(self, country, date):
        """Get new deaths for a specific country on a specific date."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT New_deaths FROM bigTable
            WHERE Country = %s AND Date_reported = %s
        """, (country, date))
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_countries(self):
        """Returns a list of all country names from bigTable."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT Country FROM bigTable ORDER BY Country;
        """)
        countries = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return countries

    def get_stats(self, country, start_date, end_date):
        """Returns daily cases and deaths for a country between two dates."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT Country, Date_reported, New_cases, New_deaths
            FROM bigTable
            WHERE Country = %s AND Date_reported >= %s AND Date_reported <= %s
            ORDER BY Date_reported
        """, (country, start_date, end_date))
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_data(self):
        """Returns all rows from bigTable as a list of dictionaries."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT Country, Date_reported, New_cases, New_deaths FROM bigTable
        """)
        rows = cursor.fetchall()
        cursor.close()

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
    results = ds.get_stats("Afghanistan", "2023-06-18", "2023-08-06")
    for row in results:
        print(row)
    ds.connection.close()
