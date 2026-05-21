# Business Memo: Retention Strategy Pre-Launch Investigation

**To:** Product, Marketing, and Customer Success Teams
**From:** Data Science & Analytics
**Date:** September 30, 2025
**Subject:** Churn Risk Patterns & Pre-Campaign Investigation Requirements

Before launching targeted retention campaigns, we have audited the customer, transaction, and behavioral data. We have identified several high-value, dataset-backed patterns that must be addressed to ensure our campaign budget is spent effectively.

## 1. Digital Engagement is the Strongest Churn Predictor
**Finding:** Customers who have not interacted with our app or website in the last 15-20 days have an elevated churn risk (~50%), which spikes to over 88% if their last visit was more than 30 days ago. 
**Action Required:** Marketing should investigate why early-stage drop-offs occur. We need to implement low-cost, automated push notifications or "we miss you" engagement triggers around day 14 of inactivity *before* the churn probability crosses the 50% threshold.

## 2. Support Ticket Volume Indicates Engagement, Not Just Friction
**Finding:** Counterintuitively, the churn rate decreases as the number of support tickets increases. Customers with 0 tickets churn at ~47%, while those with 3+ tickets churn at significantly lower rates.
**Action Required:** Customer Support should not be viewed purely as a cost center for dissatisfied customers. Highly communicative customers are engaged. We should investigate what specifically makes 0-ticket customers churn (e.g., silent abandonment) and consider proactive check-ins for customers who place orders but never interact.

## 3. High Baseline Churn in Middle-Aged Demographics
**Finding:** Customers in the 35-44 age bracket exhibit the highest baseline churn (48.3%). Additionally, general marketing consent (opt-in) does not drastically lower the churn probability, meaning our current generic newsletters are not retaining this segment.
**Action Required:** The Product team should review the core product offerings for the 35-44 demographic (e.g., Wellness and Skin Care categories). Marketing must shift from generic emails to highly personalized, category-specific content for this group.

## 4. 'New Launch' Campaigns Are Underperforming
**Finding:** Customers whose last received campaign was a 'New Launch' promotion churned at a higher rate (>51%) compared to those who received 'Welcome Offers' or 'Bundle Discounts' (~45-46%).
**Action Required:** Marketing needs to investigate the audience for 'New Launch' campaigns. Are we sending these to dormant customers who are already disengaged, effectively wasting campaign spend? We should test sending high-value 'Bundle Discounts' to at-risk segments instead of new product alerts.

## 5. Next Steps
We strongly recommend segmenting the customer base using RFM (Recency, Frequency, Monetary) metrics combined with the web-activity days-since-last-visit signal. This will allow us to prioritize our budget on "At-Risk" customers (e.g., 10-20 days since last visit) rather than "Lost" customers (>30 days).
