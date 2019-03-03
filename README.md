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
  SmartonFhir API. When clicking to see the patient's personalized info, every
  patient shows the same info, which is from: `Lorie Hessel` (one of the few
  renal patients).

- **Next steps:** Make the patients view change graphs dynamically showing
  clicked patient's info. 