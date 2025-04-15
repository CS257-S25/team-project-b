# Title
**Global COVID-19 Trends Tracker**
# Dataset(s) summary
We will use the **Weekly COVID-19 Cases and Deaths by Date Reported to WHO** dataset. This dataset contains cumulative and weekly reported cases and deaths from every country worldwide.
# Dataset(s) Metadata
- **URL:** https://data.who.int/dashboards/covid19/data
- **Date Downloaded:** 04/07/25
- **Authorship:** World Health Organization (WHO)
- **Dataset Name and Version:** Weekly COVID-19 cases and deaths by date reported to WHO
- **Terms of Use:** 
The World Health Organization (“WHO”) encourages public access and use of the data that it collects and publishes on its web site data.who.int. The data are organized in datasets and made available in machine-readable format (“Datasets”). The Datasets have been compiled from data provided by WHO’s Member States under the WHO policy on the use and sharing of data collected by WHO in Member States outside the context of public health emergencies.

Use of the data derived from the Datasets, which may appear in formats such as tables and charts, is also subject to these Terms and Conditions. Datasets may include data describing the Dataset called “Metadata”. If any datasets are credited to a source other than WHO, then those materials are not covered by these Terms and Conditions, and permission should be sought from the source provided. You are responsible for determining if this is the case, and if so, you are responsible for obtaining any necessary permission from the sources indicated. The risk of claims resulting from infringement of any third-party-owned component in the materials rests solely with you.

You may use our application programming interfaces (“APIs”) to facilitate access to the Datasets, whether through a separate web site or through another type of software application. By using the Datasets or any presentations of data derived from them, or by using our APIs in connection with the Datasets, you agree to be bound by these Terms and Conditions, as may be amended from time to time by WHO at its sole discretion.

Unless specifically indicated otherwise, these Datasets are provided to you under a Creative Commons Attribution 4.0 International License (CC BY 4.0), with the additional terms below. The basic terms applicable to the CC BY 4.0 license may be accessed here. By downloading or using the Datasets, you agree to comply with the terms of the CC BY 4.0 license, as well as the following mandatory and binding addition:

Any dispute relating to the interpretation or application of this license shall, unless amicably settled, be subject to conciliation. In the event of failure of the latter, the dispute shall be settled by arbitration. The arbitration shall be conducted in accordance with the modalities to be agreed upon by the parties or, in the absence of agreement, with the UNCITRAL Arbitration Rules. The parties shall accept the arbitral award as final.
- **Suggested Citation:**
World Health Organization 2023 data.who.int, WHO Coronavirus (COVID-19) dashboard > Data [Dashboard]. https://data.who.int/dashboards/covid19/data

# Potential User Interactions

### User Story 1
A user can compare COVID-19 cases and deaths between two  or more (up to 5) countries during a partiuclar week so that they can analyze which country was more affected during that period.

- A user can select 2+ countries from a list.
- A user can choose a week. 
- The system provides a summary of total cases and deaths for each country during the selected week.
- The user can clearly see the differences in case and death counts in a visual representation. (data is plotted for a test).

### User Story 2
A user can view COVID-19 case and death statistics over multiple weeks for a specific country so that they can track the country's experience throughout the pandemic. Up to 5 weeks can be selected (able to be ajusted).

- A user can select a country from a list.
- The system displays the weekly totals of cases and deaths for that country on the weeks selected.
- The user can view cumulative statistics across the dataset in a visual representation. (data is plotted for a test).

### User Story 3
A user can select a time period to find out which country had the highest number of COVID-19 cases and deaths during that time.

- A user can specify a date range.
- The system identifies the country with the highest number of cases and deaths within that range.
- The user receives clear numerical results and country names. 
