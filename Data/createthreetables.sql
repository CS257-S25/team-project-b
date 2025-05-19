-- Drop tables if they already exist (for repeated runs)
DROP TABLE IF EXISTS covid_data, dates, countries, staging_raw_data;

CREATE TABLE staging_raw_data (
    report_date TEXT,
    country_code TEXT,
    country_name TEXT,
    cases INT,
    deaths INT
);

CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_code TEXT UNIQUE,
    country_name TEXT
);

CREATE TABLE dates (
    date_id SERIAL PRIMARY KEY,
    report_date DATE UNIQUE
);

CREATE TABLE covid_data (
    data_id SERIAL PRIMARY KEY,
    country_id INT REFERENCES countries(country_id),
    date_id INT REFERENCES dates(date_id),
    cases INT,
    deaths INT
);
INSERT INTO countries (country_code, country_name)
SELECT DISTINCT country_code, country_name
FROM staging_raw_data
ON CONFLICT (country_code) DO NOTHING;

INSERT INTO dates (report_date)
SELECT DISTINCT TO_DATE(report_date, 'MM/DD/YY')
FROM staging_raw_data
ON CONFLICT (report_date) DO NOTHING;


INSERT INTO covid_data (country_id, date_id, cases, deaths)
SELECT
    c.country_id,
    d.date_id,
    s.cases,
    s.deaths
FROM staging_raw_data s
JOIN countries c ON s.country_code = c.country_code
JOIN dates d ON TO_DATE(s.report_date, 'MM/DD/YY') = d.report_date;
