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

"Ethiopia on 2021-10-10: 6061 cases, 275 deaths."

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
