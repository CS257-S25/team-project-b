# CS257 - 🌍 COVID-19 Statistics CLI Tool 📈
This tool allows the user to explore global COVID-19 data through the:
[WHO-COVID-19-global-data.csv](https://covid19.who.int/data)
This interface will support 3 core features, each providing insight
into case and death counts across the globe. 

# Team Members 👥:
Owen Heidtke, Daniel Zhang, Fenan Gudina, Anthony Vazquez

# User Stories📚:

## User Story #1 📖 "Compare"

Allows a user to compare total  COVID-19 cases and deaths for up to five countries during a specified week 

#### Usage:
To run this scenario, the user would input:
python3 cl.py --compare "Canada" "France" "Brazil"-- week "2021-02-15"

The output would look something like:
Canada: 21,675 cases, 390 deaths
France: 126,417 cases, 2,405 deaths 
Brazil: 316,222 cases, 7,822 deaths

## User Story #2 📖 "Change"

Allows a user to display the total weekly COVID-19 cases and deaths for a chosen country (Maximum of five)

#### Usage: 
To run this scenario, the user would input:
python3 cl.py --country "India" --weeks "2021-03-01" "2021-03-08" "2021-03-15"

The output would look something like:
Week of 2021-03-01: 103,098 cases, 1,258 deaths
Week of 2021-03-08: 117,972 cases, 1,289 deaths 
Week of 2021-03-15: 203,540 cases, 1,674 deaths

## Acceptance Tests ✅
For this project, are Acceptance Tests can be found under our "Tests" folder in a file titled "cl.py"
