-- Drop in the correct order to avoid dependency issues
DROP TABLE IF EXISTS covid;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS report_dates;

-- Table for countries
CREATE TABLE countries (
  country_id serial PRIMARY KEY,
  country_code text,
  country text
);

-- Table for dates
CREATE TABLE report_dates (
  date_id serial PRIMARY KEY,
  date_reported date
);

-- Table for covid stats
CREATE TABLE covid (
  id serial PRIMARY KEY,
  date_id int REFERENCES report_dates(date_id),
  country_id int REFERENCES countries(country_id),
  new_cases int,
  new_deaths int
);
