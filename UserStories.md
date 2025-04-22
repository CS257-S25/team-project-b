This file outlines our three core user stories and interactions supported by the COVID-19 Statistics CLI Tool.

# User Stories
User Story 1: Compare Countries During a Specific Week

**As a user**,  
The program can compare COVID-19 cases and deaths between two or more (up to 5) countries during a particular week  
**so that** I can analyze which country was more affected during that period.

### ✅ Functional Requirements:
- The user can select **2 to 5 countries** from a list.
- The user can choose a **single week** (by providing a date within that week).
- The system provides a **summary of total cases and deaths** for each selected country during that week.
## 📊 User Story 2: View Weekly Stats for One Country

**As a user**,  
The program can display COVID-19 case and death statistics over multiple weeks for a specific country  
**so that** I can track that country’s experience throughout the pandemic.

### ✅ Functional Requirements:
- The user can select **one country** from a list.
- The user can choose up to **5 weeks** (each represented by a date).
- The system displays the **weekly totals** of new cases and deaths for the country.

## Acceptance Tests
For this project, are Acceptance Tests can be found under our "Tests" folder in a file titled "test_cl.py". 

These tests are used to ensure our program is able to meet and deliver our user stories. 

#### User Story 1: Comparing Countries

The test_compare function verifies that multiple countries (up to 5) can be compared within a specified date range.

Example: Comparing "Afghanistan" and "Albania" from 2020-01-01 to 2020-01-12 should yield the correct total case and death counts.

#### User Story 2: Single Country Stats Over Time

The test_stats function checks whether accurate statistics are returned for a single country over a given time period.

The test_cl_main_stats also confirms correct CLI output for this functionality.
