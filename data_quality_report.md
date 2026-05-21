# Data Quality Report & Audit

## Overview
This report summarizes the data quality issues identified across the D2C Customer Churn dataset and details the required treatment recommendations prior to deploying any retention campaigns or machine learning models.

---

## 1. Missing Values Analysis
- **`loyalty_tier` (customers.csv):** 1,386 null values. This represents ~57.8% of the customer base. 
  - *Recommendation:* These are not missing at random; they represent customers not enrolled in the loyalty program. Impute as `"Not Enrolled"`.
- **`skin_type` (customers.csv):** 401 null values.
  - *Recommendation:* Impute as `"Unknown"` since this is an optional self-reported field.
- **`rating` (orders.csv):** 80 null values.
  - *Recommendation:* Impute with the median rating (5.0) or flag as a separate category before computing averages.

## 2. Duplicate Records
- **`order_id` (orders.csv):** 12 orders have an identical counterpart suffixed with `_DUP`.
  - *Recommendation:* These are exact duplicates simulating ETL pipeline glitches. The `_DUP` suffix should be stripped, and exact duplicate rows should be dropped entirely to prevent double-counting of revenue and order frequency.

## 3. Invalid or Unusual Values (Outliers)
- **`gross_amount` (orders.csv):** The maximum order value is ₹24,789.38, whereas the 75th percentile is only ₹907.43. 
  - *Recommendation:* A small number of extreme outliers exist. For feature engineering (like `monetary_180d`), these should either be capped (Winsorized at the 99th percentile) or left intact depending on whether the business routinely processes high-value wholesale/bulk D2C orders.

## 4. Date Consistency & Leakage Hazards (Critical)
- **Target Leakage:** The evaluation snapshot date is `2025-09-30`. The `orders.csv` table contains 1,872 orders that occurred *after* this date.
  - *Treatment:* Any row with `order_date > 2025-09-30` must be strictly excluded from the feature engineering pipeline. Using post-snapshot orders will leak the target variable (whether they made a purchase in the next 60 days) and artificially inflate model accuracy.

## 5. Join & Key Issues
- All 2,400 customers exist in the target label and web event snapshot tables.
- However, only 1,247 unique customers have raised support tickets.
  - *Treatment:* When performing a `LEFT JOIN` from `customers` to `support_tickets`, the resulting nulls should be filled with `0` for metrics like `ticket_count` and `reopened_count`, representing customers who have never required support.

---
**Conclusion:** The datasets are generally well-structured, but the leakage hazard in `orders.csv` and the presence of intentional duplicates require careful preprocessing before feeding the data into any segmentation or predictive model.
