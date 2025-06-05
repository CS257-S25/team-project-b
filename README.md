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
"python3 cl.py compare Afghanistan,Ethiopia 2021-10-10"

The output would look something like:  
Afghanistan on 2021-10-10: 203 cases, 9 deaths.

Ethiopia on 2021-10-10: 6061 cases, 275 deaths.

## User Story #2 📖 "stats"

Allows a user to display the total weekly COVID-19 cases and deaths for a chosen country (Maximum of five)

#### Usage: 
To run this scenario, the user would input:
"python3 cl.py stats Kenya 2022-01-02 2022-01-30"

The output would look something like:  
Total cases in Kenya from 2022-01-02 to 2022-01-30: 39876
Total deaths in Kenya from 2022-01-02 to 2022-01-30: 219  

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

### How our Website Enables Scanability, Satisficing, Muddling through
Our Website is scanable because it has a clear and concise homepage that has clear headings that allows the user to quickly see where our commands are. Our pages are also very minimilistic which makes it easy to use.

Satisficing. Our Website is satisficing because it allows the user to search what they want to do. We give them a list of countries for both our compare and stats methods and they can either choose or search up a country. We also provide a calendar for them to choose their date as a natural shortcut

Muddling Through. We have a help page that allows the user to seek help understanding how to operate our website if they need help. We also have a lot of redunency built into our website. We tell the user which date is the earliest possible date and we also have a very minimilistic website which allows the user to muddle through on their own fairly easily. 

### Project Design Improvements
-- Front End Design Improvements -- 
1. Usability issue was that our title/logo in the upper left corner in every page of our app looked like a home button but wasn't. Users would click on it expecting to go to the home page but that wouldn't happen, since it was just plain text. We changed the title/logo into a button that the user could press that takes them back to the home page.
2. For each our our stats and compare pages we had a line of text that told the user the specified date range but this text was too small and every time the user would not notice and input dates that were out of this range. This issue appears on our stats and compare pages and we changed these pages to where the text indicating the range of dates to be bigger and bold so that users would notice.
### Code Design Improvements
-- Code Design Improvements -- 
1. In ProductionCode/covid_stats.py (lines 54–85), a long method code smell was present in the compare function, which made the logic difficult to read and maintain. To address this, the method was refactored by extracting the country-specific data processing into a separate helper function, _get_country_stats(). This reduced the method's length, improved modularity, and enhanced clarity while preserving the original functionality.
2. Issue: Repeated if ds is None: ds = DataSource() in multiple functions (get_closest_date, get_cases_and_deaths_stats, compare)
Fix: Added a helper function get_ds(ds) at the top of covid_stats.py (around line 7) to handle default DataSource logic.
Result: Cleaner code, less repetition, easier to maintain.
