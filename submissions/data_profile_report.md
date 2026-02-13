# Data Profiling Report

## Data Overview

The dataset contains **10000 rows** and **17 columns** representing customer demographic, behavioral, and transactional data.

### Column Types

- **Numeric (5)**
  - customer_id (int64)
  - age (int64)
  - total_orders (int64)
  - total_spent (float64)
  - avg_order_value (float64)

- **Boolean (1)**
  - is_subscribed

- **String (11)**
  - first_name
  - last_name
  - email
  - phone
  - gender
  - country
  - city
  - signup_date
  - signup_source
  - segment
  - last_order_date

### Memory Usage

Approximate memory usage (deep): **~7.3 MB**

### Observations

- `signup_date` and `last_order_date` are stored as strings and should be converted to datetime.
- No duplicate customer_id values were identified.
- Text fields may require normalization (case formatting and whitespace trimming).

---

## Missing Values

The following columns contain missing values:

- **email**: 147 missing (1.47%)
- **phone**: 490 missing (4.90%)
- **gender**: 213 missing (2.13%)
- **last_order_date**: 8,162 missing (81.62%)

### Interpretation

- Missing email, phone, and gender values are relatively small (<5%).
- The high percentage of missing values in `last_order_date` likely represents customers who have not placed an order.
- No missing values exist in core transactional columns such as total_spent or total_orders.

---

## Distributions

### Numeric Columns

#### Age

- Mean: 36.07
- Min: -1
- Max: 999
- Majority between 25–45

Invalid values identified:

- 12 records with age = -1
- 14 records with age = 0
- 10 records with age = 150
- 11 records with age = 999

These are clearly invalid and require correction.

---

#### Total Orders

- 8,153 customers (81.53%) have placed 0 orders.
- Maximum orders: 90

Distribution is heavily skewed toward zero.

---

#### Total Spent

- Mean: 6,434
- Max: 550,298
- 8,162 customers (81.62%) have spent 0.

Strong right-skew with extreme outliers.

---

#### Average Order Value

- Mean: 1,666
- Max: 84,598
- Majority are 0 due to no purchases.

Contains significant high-value outliers.

---

## Outliers

The following suspicious values were identified:

- Age values of -1, 0, 150, and 999.
- Maximum total_spent of 550,298.
- Maximum avg_order_value of 84,598.
- One customer with 90 total orders.

These values may represent data entry errors or exceptional customers and should be investigated.

---

## Data Quality Issues

1. **Invalid Age Values**
   - Negative and unrealistic ages present.

2. **Phone Number Inconsistencies**
   - Multiple formats (local, international, extensions, parentheses, missing values).
   - Not standardized.

3. **Invalid Email Formats**
   - Examples include clearly invalid emails (e.g., missing '@').
   - Inconsistent casing observed.

4. **Date Columns Stored as Strings**
   - signup_date and last_order_date should be converted to datetime format.

5. **Text Formatting Issues**
   - Trailing spaces in some city names.
   - Case inconsistencies in email fields.

---

## Logical Consistency Checks

- Customers with total_orders = 0 consistently have:
  - total_spent = 0
  - avg_order_value = 0
  - missing last_order_date

No major transactional inconsistencies were identified.

---

## Recommendations

1. Remove or correct invalid age values (-1, 0, 150, 999).
2. Convert date columns to datetime format.
3. Standardize phone numbers into a consistent international format.
4. Validate email formats using regex and normalize to lowercase.
5. Trim whitespace from string fields.
6. Investigate extreme spending and order outliers.
7. Segment customers into:
   - Non-purchasers (81%)
   - Active purchasers (19%)
8. Define handling strategy for missing gender values (e.g., impute as "Unknown").

---

## Overall Assessment

The dataset is structurally sound and internally consistent but contains several data quality issues including invalid demographic values, formatting inconsistencies, and extreme financial outliers.

After cleaning and normalization, the dataset will be suitable for reliable analytics, segmentation, and revenue modeling.
