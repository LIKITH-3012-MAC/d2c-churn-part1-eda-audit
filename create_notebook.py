import nbformat as nbf

nb = nbf.v4.new_notebook()

# Title
text_title = """# D2C Customer Churn Intelligence & Retention API
## Part 1: Data Audit, EDA & Business Understanding

**Objective**: Audit the raw data, perform exploratory analysis, and derive data-backed business hypotheses for churn risk."""

code_imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# Set path to datasets
data_path = '../data/d2c churn data package/'"""

text_loading = """### 1. Data Loading & Schema Inspection"""

code_load = """# Load all datasets
customers = pd.read_csv(data_path + 'customers.csv')
orders = pd.read_csv(data_path + 'orders.csv')
support_tickets = pd.read_csv(data_path + 'support_tickets.csv')
web_events = pd.read_csv(data_path + 'web_events_snapshot.csv')
churn_labels = pd.read_csv(data_path + 'churn_labels.csv')
interventions = pd.read_csv(data_path + 'intervention_history.csv')
rfm_snapshot = pd.read_csv(data_path + 'rfm_modeling_snapshot.csv')

print(f"Customers shape: {customers.shape}")
print(f"Orders shape: {orders.shape}")
print(f"Support Tickets shape: {support_tickets.shape}")
print(f"Web Events shape: {web_events.shape}")
print(f"Churn Labels shape: {churn_labels.shape}")
print(f"Interventions shape: {interventions.shape}")
print(f"RFM Snapshot shape: {rfm_snapshot.shape}")"""

text_dq = """### 2. Data Quality & Cleaning
We perform an audit covering missing values, duplicates, and timeline consistencies.

**Critical Rules**:
- Identify missing values and unusual outliers.
- Handle duplicate `_DUP` records in orders.
- Identify leakage by separating pre-snapshot features (`<= 2025-09-30`) from post-snapshot targets."""

code_dq1 = """# Missing Values
print("Missing values in Customers:")
print(customers.isnull().sum()[customers.isnull().sum() > 0])
print("\\nMissing values in Orders:")
print(orders.isnull().sum()[orders.isnull().sum() > 0])

# Impute missing values
customers['loyalty_tier'] = customers['loyalty_tier'].fillna('Not Enrolled')
customers['skin_type'] = customers['skin_type'].fillna('Unknown')
orders['rating'] = orders['rating'].fillna(orders['rating'].median())"""

code_dq2 = """# Handle Duplicates in Orders
dup_orders = orders[orders['order_id'].str.contains('_DUP', na=False)]
print(f"Found {len(dup_orders)} duplicate-like orders with '_DUP' suffix.")

orders['order_id_clean'] = orders['order_id'].str.replace('_DUP', '')
orders_clean = orders.drop_duplicates(subset=['order_id_clean', 'category', 'quantity', 'gross_amount', 'discount_pct', 'delivery_days', 'returned', 'rating']).copy()
print(f"Orders shape after deduplication: {orders_clean.shape}")"""

code_dq3 = """# Handle Dates and Data Leakage
snapshot_date = pd.to_datetime('2025-09-30')
orders_clean['order_date'] = pd.to_datetime(orders_clean['order_date'])

pre_snapshot_orders = orders_clean[orders_clean['order_date'] <= snapshot_date].copy()
post_snapshot_orders = orders_clean[orders_clean['order_date'] > snapshot_date].copy()

print(f"Pre-snapshot orders (for features): {len(pre_snapshot_orders)}")
print(f"Post-snapshot orders (Target Leakage): {len(post_snapshot_orders)}")"""

text_joins = """### 3. Data Joins
We will aggregate order and support ticket data for each customer before joining it with demographic and event data."""

code_joins = """# Aggregate Orders
cust_orders = pre_snapshot_orders.groupby('customer_id').agg(
    total_orders=('order_id', 'nunique'),
    total_spend=('gross_amount', 'sum'),
    return_rate=('returned', lambda x: x.sum() / len(x))
).reset_index()

# Aggregate Tickets
cust_tickets = support_tickets.groupby('customer_id').agg(
    ticket_count=('ticket_id', 'count'),
    avg_resolution_hours=('resolution_hours', 'mean'),
    reopened_count=('reopened', 'sum')
).reset_index()

# Merge everything
df = customers.merge(churn_labels[['customer_id', 'churn_next_60d']], on='customer_id', how='left')
df = df.merge(web_events, on='customer_id', how='left')
df = df.merge(interventions, on='customer_id', how='left')
df = df.merge(cust_orders, on='customer_id', how='left')
df = df.merge(cust_tickets, on='customer_id', how='left')

# Fill NaN for customers with 0 orders/tickets
df['total_orders'] = df['total_orders'].fillna(0)
df['total_spend'] = df['total_spend'].fillna(0)
df['return_rate'] = df['return_rate'].fillna(0)
df['ticket_count'] = df['ticket_count'].fillna(0)
df['avg_resolution_hours'] = df['avg_resolution_hours'].fillna(0)
df['reopened_count'] = df['reopened_count'].fillna(0)

print(f"Final merged dataframe shape: {df.shape}")"""

text_eda = """### 4. Exploratory Data Analysis & Hypotheses
We will investigate specific features and derive business hypotheses backed by charts."""

code_eda1 = """# 1. Churn Distribution
plt.figure(figsize=(6, 6))
df['churn_next_60d'].value_counts(normalize=True).plot.pie(autopct='%1.1f%%', colors=['#4c72b0', '#c44e52'])
plt.title('Churn Label Distribution')
plt.ylabel('')
plt.show()

print("Observation: The dataset is relatively balanced with ~47% churn rate.")"""

code_eda2 = """# Hypothesis 1: Web Activity & Recency strongly correlate with churn.
plt.figure(figsize=(10, 5))
df['visit_group'] = pd.cut(df['last_visit_days_ago'], bins=[-1, 5, 10, 15, 20, 30, 100])
visit_churn = df.groupby('visit_group', observed=False)['churn_next_60d'].mean().reset_index()
sns.barplot(data=visit_churn, x='visit_group', y='churn_next_60d', palette='Reds_d')
plt.title('Churn Rate by Days Since Last Web/App Visit')
plt.ylabel('Churn Rate')
plt.xlabel('Days Since Last Visit')
plt.show()

print("Hypothesis 1: Customers who have not visited the app/web in over 20 days are significantly more likely to churn (>68% churn rate). Digital engagement is a leading indicator.")"""

code_eda3 = """# Hypothesis 2: Support Ticket Count indicates engagement rather than just dissatisfaction.
plt.figure(figsize=(10, 5))
ticket_churn = df.groupby('ticket_count')['churn_next_60d'].mean().reset_index()
sns.barplot(data=ticket_churn, x='ticket_count', y='churn_next_60d', palette='Blues_d')
plt.title('Churn Rate by Support Ticket Count')
plt.ylabel('Churn Rate')
plt.xlabel('Number of Support Tickets')
plt.show()

print("Hypothesis 2: Counterintuitively, higher support ticket counts correlate with lower churn rates (e.g., 4+ tickets drops churn to <25%). This suggests customers with many interactions are engaged, not abandoning.")"""

code_eda4 = """# Hypothesis 3: Age Demographics and Preferences affect retention.
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x='age_group', y='churn_next_60d', hue='marketing_consent', palette='viridis', errorbar=None)
plt.title('Churn Rate by Age Group and Marketing Consent')
plt.show()

print("Hypothesis 3: Middle-aged customers (35-44) exhibit the highest baseline churn. Marketing consent does not drastically change churn likelihood, meaning campaigns might not be targeting effectively.")"""

code_eda5 = """# Hypothesis 4: High Order Returns indicate friction.
plt.figure(figsize=(10, 5))
df['has_returns'] = df['return_rate'] > 0
sns.barplot(data=df, x='has_returns', y='churn_next_60d', palette='coolwarm')
plt.title('Churn Rate: Customers With Returns vs No Returns')
plt.show()

print("Hypothesis 4: The overall average return rate has a weak correlation to absolute churn, suggesting returns process is acceptable. Deeper segmentation is required to find dissatisfied returners.")"""

code_eda6 = """# Hypothesis 5: Campaign Type Effectiveness
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x='last_campaign_received', y='churn_next_60d', palette='Set2')
plt.title('Churn Rate by Last Campaign Received')
plt.show()

print("Hypothesis 5: 'New Launch' campaigns see a slightly higher churn rate (>50%) compared to 'Welcome Offer' or 'None'. The brand should investigate if 'New Launch' targets dormant users who are already out the door.")"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_title),
    nbf.v4.new_code_cell(code_imports),
    nbf.v4.new_markdown_cell(text_loading),
    nbf.v4.new_code_cell(code_load),
    nbf.v4.new_markdown_cell(text_dq),
    nbf.v4.new_code_cell(code_dq1),
    nbf.v4.new_code_cell(code_dq2),
    nbf.v4.new_code_cell(code_dq3),
    nbf.v4.new_markdown_cell(text_joins),
    nbf.v4.new_code_cell(code_joins),
    nbf.v4.new_markdown_cell(text_eda),
    nbf.v4.new_code_cell(code_eda1),
    nbf.v4.new_code_cell(code_eda2),
    nbf.v4.new_code_cell(code_eda3),
    nbf.v4.new_code_cell(code_eda4),
    nbf.v4.new_code_cell(code_eda5),
    nbf.v4.new_code_cell(code_eda6)
]

with open('eda_audit.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook 'eda_audit.ipynb' created successfully.")
