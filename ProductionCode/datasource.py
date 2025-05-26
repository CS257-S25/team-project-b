"""Module to handle database connection and COVID-19 data queries."""

import sys
import psycopg2
import ProductionCode.psql_config as config


class DataSource:
    """Handles database connection and data operations for COVID statistics."""

    def __init__(self):
        """Initialize connection to the database."""
        self.connection = self.connect()

    def connect(self):
        """Connects to the database using credentials from config.
        Returns the connection object."""
        try:
            return psycopg2.connect(
                database=config.DATABASE,
                user=config.USER,
                password=config.PASSWORD,
                host="localhost"
            )
        except psycopg2.OperationalError as e:
            sys.exit(
                f"Unable to connect to the database. Error: {e}. "
                "Please check your connection settings."
            )

    def get_sum_between_dates(self, country, start_date, end_date):
        """Returns sum of cases and deaths for a country between two dates."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(cd.cases), SUM(cd.deaths)
                FROM covid_data AS cd
                JOIN countries AS c ON cd.country_id = c.id
                JOIN dates AS d ON cd.date_id = d.id
                WHERE c.country_name = %s AND d.report_date BETWEEN %s AND %s
            """, (country, start_date, end_date))
            return cursor.fetchone()

    def get_sum_specific(self, country, date):
        """Returns cases and deaths for a country on a specific date."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(cd.cases), SUM(cd.deaths)
                FROM covid_data AS cd
                JOIN countries AS c ON cd.country_id = c.id
                JOIN dates AS d ON cd.date_id = d.id
                WHERE c.country_name = %s AND d.report_date = %s
            """, (country, date))
            return cursor.fetchone()

    def get_closest_date(self, target_date, country, before=True):
        """Returns the closest available date for a country."""
        try:
            with self.connection.cursor() as cursor:
                if before:
                    query = """
                        SELECT MAX(d.report_date)
                        FROM covid_data AS cd
                        JOIN countries AS c ON cd.country_id = c.id
                        JOIN dates AS d ON cd.date_id = d.id
                        WHERE c.country_name = %s AND d.report_date <= %s
                    """
                else:
                    query = """
                        SELECT MIN(d.report_date)
                        FROM covid_data AS cd
                        JOIN countries AS c ON cd.country_id = c.id
                        JOIN dates AS d ON cd.date_id = d.id
                        WHERE c.country_name = %s AND d.report_date >= %s
                    """
                cursor.execute(query, (country, target_date))
                result = cursor.fetchone()
                return result[0] if result and result[0] else None
        except psycopg2.OperationalError as e:
            print("Error finding closest date:", e)
            return None

    def get_week_country_and_new_cases(self, country, date):
        """Returns number of new cases for a country on a given date."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT cd.cases
                FROM covid_data AS cd
                JOIN countries AS c ON cd.country_id = c.id
                JOIN dates AS d ON cd.date_id = d.id
                WHERE c.country_name = %s AND d.report_date = %s
            """, (country, date))
            return cursor.fetchall()

    def get_week_country_and_new_deaths(self, country, date):
        """Returns number of new deaths for a country on a given date."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT cd.deaths
                FROM covid_data AS cd
                JOIN countries AS c ON cd.country_id = c.id
                JOIN dates AS d ON cd.date_id = d.id
                WHERE c.country_name = %s AND d.report_date = %s
            """, (country, date))
            return cursor.fetchall()

    def get_all_countries(self):
        """Returns a sorted list of all country names."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT country_name
                FROM countries
                ORDER BY country_name
            """)
            return [row[0] for row in cursor.fetchall()]

    def get_stats(self, country, beginning_date, ending_date):
        """Returns country, date, cases, and deaths between two dates."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.country_name, d.report_date, cd.cases, cd.deaths
                FROM covid_data AS cd
                JOIN countries AS c ON cd.country_id = c.id
                JOIN dates AS d ON cd.date_id = d.id
                WHERE c.country_name = %s
                  AND d.report_date > %s
                  AND d.report_date < %s
            """, (country, beginning_date, ending_date))
            return cursor.fetchall()

    def get_all_data(self):
        """Returns all COVID data including country and report date."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.country_name, d.report_date, cd.cases, cd.deaths
                FROM covid_data AS cd
                JOIN countries AS c ON cd.country_id = c.id
                JOIN dates AS d ON cd.date_id = d.id
            """)
            rows = cursor.fetchall()

        return [
            {
                "Country": row[0],
                "Date_reported": row[1],
                "New_cases": row[2],
                "New_deaths": row[3]
            }
            for row in rows
        ]


if __name__ == "__main__":
    data_source = DataSource()
    data_source.connection.close()
