# CS257 - 🌍 COVID-19 Statistics CLI Tool 📈
This tool allows the user to explore global COVID-19 data through the:
[WHO-COVID-19-global-data.csv](https://covid19.who.int/data)
This interface will support 3 core features, each providing insight
into case and death counts across the globe. 

# Team Members 👥:
Owen Heidtke, Daniel Zhang, Fenan Gudina, Anthony Vazquez

# User Stories📚:

## User Story #1 📖 "compare"

Allows a user to compare total  COVID-19 cases and deaths for up to five countries during a specified week 

#### Usage:
To run this scenario, the user would input:
"python3 cl.py compare GB,US 2021-10-10"

The output would look something like:
Total cases in GB during 2021-10-10: 254728
Total deaths in GB from 2021-10-10: 840
Total cases in US during 2021-10-10: 681984
Total deaths in US from 2021-10-10: 11684

## User Story #2 📖 "stats"

Allows a user to display the total weekly COVID-19 cases and deaths for a chosen country (Maximum of five)

#### Usage: 
To run this scenario, the user would input:

"python3 cl.py stats US 2022-01-01 2022-02-01"

The output would look something like:
Total cases in US from 2022-01-01 to 2022-02-01: 21878018!
Total deaths in US from 2022-01-01 to 2022-02-01: 69953!

# Acceptance Tests ✅
For this project, our Acceptance Tests can be found under the "Tests" folder in files titled "test_cl.py" and "test_app.py".

### Purpose of Acceptance Tests
Acceptance tests are designed to ensure that the tool meets the requirements outlined in the user stories. These tests simulate real-world usage scenarios to verify that the tool behaves as expected.

### How They Relate to User Stories
1. **User Story #1: compare**
   - The `test_cl.py` file contains tests for the `compare` feature.
   - These tests verify that the tool correctly compares COVID-19 statistics for up to five countries during a specified week.
   - Example: The test ensures that running the command `python3 cl.py compare GB,US 2021-10-10"` produces the expected output format and data.

2. **User Story #2: stats**
   - The `test_cl.py` file also includes tests for the `--stats` feature.
   - These tests validate that the tool displays weekly COVID-19 cases and deaths for a chosen country over multiple weeks.
   - Example: The test ensures that running the command `python3 cl.py stats US 2022-01-01 2022-02-01` produces the correct weekly statistics.

### How to Run the Tests
To run the acceptance tests, use the following command in the terminal:

python3 -m unittest Tests/test_cl.py

This will execute the tests and confirm whether the tool behaves as expected for the scenarios described in the user stories.
