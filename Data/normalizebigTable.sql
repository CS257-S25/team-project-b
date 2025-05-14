-- Insert unique countries
INSERT INTO countries (country_code, country)
SELECT DISTINCT country_code, country
FROM bigTable;

-- Insert unique dates
INSERT INTO report_dates (date_reported)
SELECT DISTINCT date_reported
FROM bigTable;

-- Insert into covid table
INSERT INTO covid (date_id, country_id, new_cases, new_deaths)
SELECT
  d.date_id,
  c.country_id,
  b.new_cases,
  b.new_deaths
FROM bigTable b
JOIN countries c ON b.country_code = c.country_code AND b.country = c.country
JOIN report_dates d ON b.date_reported = d.date_reported;
