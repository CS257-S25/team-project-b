-- Drop tables if they already exist (for repeated runs)

DROP TABLE IF EXISTS covid_data, dates, countries;

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    country_code TEXT UNIQUE,
    country_name TEXT
);

CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    report_date DATE UNIQUE
);

CREATE TABLE covid_data (
    data_id SERIAL PRIMARY KEY,
    country_id int NOT NULL,
    date_id int NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id),
    FOREIGN KEY (date_id) REFERENCES dates(id),
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
    c.id,
    d.id,
    s.cases,
    s.deaths
FROM staging_raw_data s
JOIN countries c ON s.country_code = c.country_code 
JOIN dates d ON TO_DATE(s.report_date, 'MM/DD/YY') = d.report_date;
