# Part 1: Data Audit, EDA & Business Understanding

Audits the raw D2C dataset, cleans data quality issues, and establishes churn-risk hypotheses.

## 1. Repository Structure
```
.
├── data/
│   └── d2c_churn_data_package/
│       ├── customers.csv
│       ├── orders.csv
│       ├── support_tickets.csv
│       ├── rfm_modeling_snapshot.csv
│       └── ...
├── README.md
├── requirements.txt
└── (Notebooks and Scripts)
```

## 2. Dataset Location
The original dataset package is securely bundled inside the repository under `data/d2c_churn_data_package/`. 
All notebooks and scripts use relative paths to automatically load the data from this directory without requiring any modifications.

## 3. Installation Command
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Run Command
Execute the following to run this part:
```bash
jupyter notebook eda_audit.ipynb
```

## 5. Expected Outputs
Upon successful execution, you should expect:
Rendered notebook with visualizations and business hypotheses.
