# Part 1: Data Audit, EDA & Business Understanding

## Project Overview
This repository contains the first part of the D2C Customer Churn Intelligence & Retention API Capstone project. The objective is to audit raw datasets, perform exploratory data analysis, evaluate data quality, and construct data-backed business hypotheses regarding customer churn.

## File Structure
- `eda_audit.ipynb`: Jupyter notebook containing the full analysis flow, dataset loading, schema inspection, feature aggregations, data joins, and visualizations forming the churn hypotheses.
- `data_quality_report.md`: A structured summary detailing missing values, duplicate records, outliers, target leakage hazards, and the recommended preprocessing treatments.
- `business_memo.md`: A concise, business-facing document outlining actionable recommendations and summarizing the key churn-risk patterns identified during the EDA.
- `requirements.txt`: Python dependencies required to run the notebook.

## Setup Instructions
1. This project part is meant to be a standalone repository.
2. Ensure Python 3.9+ is installed.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Data Placement:** Place the original dataset package inside a `data/` folder one directory level above this repository, specifically at `../data/d2c churn data package/`. This maintains a strict relative path without hardcoding absolute paths.
5. Run the Jupyter Notebook:
   ```bash
   jupyter notebook eda_audit.ipynb
   ```

## Summary of Major Findings
- **Data Quality Warnings**: The `orders.csv` file contains post-snapshot records (after `2025-09-30`) which must be excluded during model feature generation to prevent target leakage. It also contains explicit `_DUP` duplicates that require cleaning.
- **Digital Engagement**: Recency of web/app visits is the strongest leading indicator of churn.
- **Support Interactions**: Customers engaging with support have surprisingly lower churn rates, indicating that silence (zero support tickets) might be a stronger indicator of silent abandonment.
- **Demographics**: Customers aged 35-44 show the highest baseline churn.
