DROP TABLE IF EXISTS covid;

CREATE TABLE covid (
  date_id int,
  country_id int,
  new_cases int,
  new_deaths int,
);

CREATE TABLE countries (
  country_id int,
  country_code text,
  country text,
);

CREATE TABLE date (
  date_reported date,
  date_id int,
);