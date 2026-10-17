# E-commerce Sales Forecasting & Business Analytics

An end-to-end data analytics and forecasting portfolio project that analyzes e-commerce sales performance using **Python, SQL, SQLite, Pandas, Plotly, Streamlit, and time-series forecasting**.

## Live Dashboard

**Streamlit App:** https://asraiyani-ecommerce-sales-forecasting.streamlit.app/

**GitHub Repository:** https://github.com/ASRAIYANI/ecommerce-sales-forecasting

The project transforms transactional sales data into business KPIs, SQL-based analytical reports, interactive visualizations, and a six-month revenue forecast.

> **Note:** The dataset used in this project is synthetic and intended for educational and portfolio purposes. The findings should not be interpreted as evidence about a real business.

---

## Project Objectives

The project was developed to answer practical business questions such as:

- How much revenue and profit is the business generating?
- How is revenue changing year over year?
- Which categories and products generate the most revenue?
- Which regions perform best?
- Which sales channels contribute the most revenue?
- How do different discount levels relate to revenue and profitability?
- Which forecasting approach performs best on historical holdout data?
- What revenue could be expected over the next six months?

---

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **SQL**
- **SQLite**
- **Statsmodels**
- **Plotly**
- **Streamlit**
- **Git / GitHub**

---

## Project Workflow

```text
Synthetic E-commerce Dataset
            |
            v
     Data Validation
            |
            v
   Python/Pandas Analysis
            |
            +--------------------+
            |                    |
            v                    v
     SQLite Database       Time-Series Analysis
            |                    |
            v                    v
      SQL Analysis        Forecast Comparison
            |                    |
            v                    v
     SQL CSV Reports      Selected Forecast
            |                    |
            +----------+---------+
                       |
                       v
              Streamlit Dashboard
```

---

## Dataset

The dataset contains **1,096 orders** covering:

**1 January 2023 to 31 December 2025**

### Dataset fields

- `order_id`
- `order_date`
- `product`
- `category`
- `region`
- `sales_channel`
- `quantity`
- `unit_price`
- `discount`
- `revenue`
- `cost`
- `profit`

The dataset contains no missing values or duplicate rows in the validated source data.

---

## Business KPIs

The analysis produced the following overall results:

| KPI | Result |
|---|---:|
| Total Orders | 1,096 |
| Total Revenue | 1,035,889.75 |
| Total Profit | 345,852.58 |
| Profit Margin | 33.39% |
| Units Sold | 4,900 |
| Average Order Value | 945.15 |
| Average Items per Order | 4.47 |

---

## Yearly Performance

| Year | Revenue | Profit | Revenue Growth |
|---|---:|---:|---:|
| 2023 | 347,107.00 | 114,098.58 | — |
| 2024 | 303,842.25 | 102,134.38 | -12.46% |
| 2025 | 384,940.50 | 129,619.62 | +26.69% |

Revenue declined in 2024 before recovering strongly in 2025.

2025 revenue increased by approximately **26.69% year over year**, while profit increased by approximately **26.91%**.

---

## Category Analysis

| Category | Revenue | Revenue Share |
|---|---:|---:|
| Computers | 749,567.50 | 72.36% |
| Accessories | 98,990.75 | 9.56% |
| Furniture | 83,493.00 | 8.06% |
| Audio | 51,946.00 | 5.01% |
| Storage | 51,892.50 | 5.01% |

The **Computers** category generates approximately **72.36% of total revenue**, making it the dominant revenue contributor in this synthetic dataset.

This also indicates substantial revenue concentration in one category.

---

## Product Performance

The highest-revenue products are:

| Product | Revenue | Profit |
|---|---:|---:|
| Laptop | 625,982.50 | 210,940.90 |
| Monitor | 123,585.00 | 40,255.24 |
| Office Chair | 83,493.00 | 27,302.87 |
| Headphones | 51,946.00 | 17,293.75 |
| SSD | 51,892.50 | 17,244.74 |

**Laptop** is the largest individual revenue contributor in the dataset.

---

## Regional Performance

| Region | Revenue | Profit |
|---|---:|---:|
| East | 274,349.00 | 90,609.18 |
| North | 268,289.25 | 90,989.11 |
| South | 248,089.75 | 81,862.08 |
| West | 245,161.75 | 82,392.21 |

The **East** region generates the highest revenue, although revenue is relatively balanced across the four regions.

---

## Sales Channel Analysis

| Sales Channel | Revenue | Revenue Share |
|---|---:|---:|
| Website | 455,196.00 | 43.94% |
| Marketplace | 334,704.75 | 32.31% |
| Mobile App | 245,989.00 | 23.75% |

The **Website** is the largest sales channel by revenue.

---

# SQL Analytics

The project includes a SQLite analytics workflow.

The source CSV is loaded into:

```text
data/ecommerce.db
```

with the main table:

```text
orders
```

The database is generated using:

```text
src/create_database.py
```

SQL analysis demonstrates:

- `SELECT`
- `GROUP BY`
- `ORDER BY`
- aggregate functions
- subqueries
- Common Table Expressions (CTEs)
- SQLite date functions
- window functions
- `LAG()` for year-over-year analysis

SQL-generated reports include:

```text
reports/sql_overall_kpis.csv
reports/sql_yearly_performance.csv
reports/sql_category_performance.csv
reports/sql_product_performance.csv
reports/sql_region_performance.csv
reports/sql_channel_performance.csv
reports/sql_monthly_performance.csv
```

This provides a reproducible workflow:

```text
CSV -> SQLite -> SQL Queries -> Analytical Reports
```

---

# Revenue Forecasting

Monthly revenue was aggregated from the transactional dataset.

Because only **36 months of historical data** are available, several forecasting approaches were compared rather than assuming that a more complex model would perform better.

The final six months of historical data were used as a holdout test period.

## Models Compared

Four forecasting approaches were evaluated:

1. Naive Forecast
2. Seasonal Naive Forecast
3. 3-Month Moving Average
4. Holt-Winters Exponential Smoothing

### Holdout Results

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Seasonal Naive | 6,117.67 | 7,178.56 | **23.72%** |
| 3-Month Moving Average | 16,146.39 | 17,072.62 | 62.10% |
| Naive | 20,998.88 | 21,514.24 | 79.34% |
| Holt-Winters | 48,344.76 | 50,637.20 | 181.66% |

The **Seasonal Naive** model achieved the lowest holdout MAPE and was therefore selected for the final forecast.

An important lesson from this experiment is that **model complexity does not automatically produce better forecasts**.

---

## Six-Month Revenue Forecast

Using the selected Seasonal Naive approach:

| Month | Forecast Revenue |
|---|---:|
| January 2026 | 27,837.75 |
| February 2026 | 29,465.75 |
| March 2026 | 32,981.25 |
| April 2026 | 31,217.75 |
| May 2026 | 44,777.50 |
| June 2026 | 49,236.25 |

### Total Forecast Revenue

**215,516.25**

for January through June 2026.

---

# Interactive Streamlit Dashboard

The Streamlit application provides an interactive interface for exploring the business data.

### Dashboard features

- Date-range filtering
- Category filtering
- Region filtering
- Sales-channel filtering
- Revenue KPI
- Profit KPI
- Profit margin
- Order volume
- Units sold
- Average order value
- Monthly revenue and profit trends
- Yearly performance
- Category analysis
- Regional analysis
- Sales-channel analysis
- Product performance
- Discount analysis
- Six-month revenue forecast
- Forecast-model comparison
- Business insights

---

# Project Structure

```text
ecommerce_sales_forecasting_project/
|
|-- app/
|   `-- app.py
|
|-- data/
|   `-- ecommerce_orders.csv
|
|-- reports/
|   |-- category_performance.csv
|   |-- channel_performance.csv
|   |-- discount_analysis.csv
|   |-- forecast_model_comparison.csv
|   |-- monthly_kpis.csv
|   |-- product_performance.csv
|   |-- region_performance.csv
|   |-- revenue_forecast.csv
|   |-- sql_category_performance.csv
|   |-- sql_channel_performance.csv
|   |-- sql_monthly_performance.csv
|   |-- sql_overall_kpis.csv
|   |-- sql_product_performance.csv
|   |-- sql_region_performance.csv
|   |-- sql_yearly_performance.csv
|   `-- yearly_kpis.csv
|
|-- sql/
|   `-- business_analysis.sql
|
|-- src/
|   |-- analyze.py
|   |-- compare_forecasts.py
|   |-- create_database.py
|   |-- forecast.py
|   `-- run_sql_analysis.py
|
|-- .gitignore
|-- README.md
`-- requirements.txt
```

The SQLite database is generated locally and excluded from version control.

---

# How to Run the Project

## 1. Create a virtual environment

```bash
python -m venv .venv
```

## 2. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation, the Python executable inside the environment can be used directly.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run Python business analysis

```bash
python src/analyze.py
```

## 5. Create the SQLite database

```bash
python src/create_database.py
```

## 6. Run SQL analytics

```bash
python src/run_sql_analysis.py
```

## 7. Compare forecasting models

```bash
python src/compare_forecasts.py
```

## 8. Generate the final forecast

```bash
python src/forecast.py
```

## 9. Launch the Streamlit dashboard

```bash
streamlit run app/app.py
```

---

# Key Business Insights

1. Total historical revenue is approximately **1.04 million** in the dataset.

2. Revenue decreased by **12.46% in 2024** before increasing by **26.69% in 2025**.

3. Computers account for **72.36% of total revenue**, indicating that business performance is heavily influenced by this category.

4. Laptop sales are the largest individual revenue contributor.

5. The Website channel contributes approximately **43.94% of revenue**, making it the largest sales channel.

6. Regional revenue is comparatively balanced, with the East generating the highest revenue.

7. Discount-level results do not show a simple monotonic relationship between discount size and profit margin in this synthetic dataset, so the analysis should not be interpreted as evidence that discounts cause profitability changes.

8. Seasonal Naive substantially outperformed Holt-Winters on the selected six-month holdout period.

---

# Limitations

This project has several important limitations:

- The dataset is **synthetic** and created for educational purposes.
- Business findings should not be generalized to real companies.
- The forecasting dataset contains only **36 monthly observations**.
- Forecast evaluation uses a single six-month holdout period.
- More robust production forecasting would require additional historical data and techniques such as rolling-origin validation.
- External drivers such as promotions, holidays, macroeconomic conditions, inventory availability, and marketing spend are not included.

---

# Skills Demonstrated

This project demonstrates practical experience with:

- Python programming
- Pandas data analysis
- SQL analytics
- SQLite databases
- Business KPI development
- Exploratory data analysis
- Time-series aggregation
- Forecast model evaluation
- MAE, RMSE and MAPE
- Forecast model selection
- Data visualization
- Plotly
- Streamlit dashboard development
- Business insight generation
- Reproducible analytics workflows
- Git and GitHub project organization

---

## Portfolio Purpose

This project was created as a portfolio project to demonstrate an end-to-end analytics workflow covering:

**data preparation -> SQL analysis -> business intelligence -> forecasting -> interactive dashboard**

It is designed to demonstrate skills relevant to entry-level roles such as:

- Data Analyst
- Business Data Analyst
- Junior Data Scientist
- Junior Data Analyst
- BI Analyst