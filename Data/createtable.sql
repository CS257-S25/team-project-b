DROP TABLE IF EXISTS bigTable;

CREATE TABLE  bigTable(
  Date_reported date,
  Country_code text,
  Country text,
  WHO_region text,
  New_cases int,
  Cumulative_cases int,
  New_deaths int,
  Cumulative_deaths int
);