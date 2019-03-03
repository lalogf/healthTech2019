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

### App Status

- **Current state:** In the '/' route the app shows a list of patients from
  SmartonFhir API. Only when clicking: `Lorie Hessel` (first patient in list)
  the app will show relevant renal disease measurements like: `Urea Nitrogen`,
  `Creatinine `, `Body Mass Index`, `Blood Pressure`,`Estimated Glomerular
  Filtration Rate`. For other patients, the app will show all the observations
  that the API gives.

- **Next steps:** identify more renal patients.
