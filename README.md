# Health Tech web app


**Live app:** [here](https://ht-kidney-disease.herokuapp.com/)

## Intro

Through our research we found that managing chronic kidney disease is especially
difficult given the fact that it is tightly linked with many other health-issues
such as hypertension, diabetes, diet etc. These vitals are constantly changing
and so is the medication taken to control them. Thus physicians have a tougher
time diagnosing care plans to patients as it is difficult to digest this
historical data along with all the lab results that many CKD patients generate.
We would like to build a tool that allows physicians to view the historical
trends of these key metrics such as blood pressure, creatinine levels,
etc.

In this first version, when clicking `Lorie Hessel` (first patient in list)
the app will show relevant renal disease measurements like: `Urea Nitrogen`,
`Creatinine `, `Body Mass Index`, `Blood Pressure`,`Estimated Glomerular
Filtration Rate`. For other patients, the app will show all the observations
that the API gives.

Patient Blood Pressure visualization

![app-image](https://lh5.googleusercontent.com/TVCH9plTR3g4_15sUgEqp93EZHZDDMsDMflGCJLrQ6RyWlsn8RZStIBPMz1JPTehgVbZyj4bqm_EUReJvT8kQC1nxNf4TSXOlYRXOOOGqd5IAaspdnzR8QwNJPzJhAiFiiNC1mNhGvw)


Patient Urea Nitrogen visualization

![demo-image](https://lh3.googleusercontent.com/8HHgSrhL90v34G19LABSpsW3C9pGAwbGRUxcZJcMcs32EMZDRoB0FaXrmeHNEGyf0VkxnpTdtvWzzFua18X9PBC9J1JwW_idsgI9nb1QIFBbuyslDBPJ5jB_Z6B11H4WgXqvqReoJbM)

## App Status

- **Current state:** In the '/' route the app shows a list of patients from
  SmartonFhir API. Only when clicking first patient in list the app will show
  relevant renal disease measurements. For other patients, the app will show all
  the observations that the SmartonFhir API gives.

- **Next steps:** identify more renal patients.

## Installation

1. Clone the repo into a directory of your choice and step into it.
2. Ensure you have pip installed on your computer and then install the following packages:

```bash
pip install dash==0.38.0  # The core dash backend
pip install dash-html-components==0.13.5  # HTML components
pip install dash-core-components==0.43.1  # Supercharged components
pip install dash-table==3.5.0  # Interactive DataTable component (new!)
pip install dash-daq==0.1.0  # DAQ components (newly open-sourced!)
pip install dash_bootstrap_components # Bootstrap CSS and components
```


3. Then run in the directory where the repo was cloned: 

```bash
python app.py
```

4. Then go to the portal specified in your terminal (example output: Running on http://127.0.0.1:8050/)


