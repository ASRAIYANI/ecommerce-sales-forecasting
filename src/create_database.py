from pathlib import Path
import sqlite3
import pandas as pd


BASE = Path(__file__).resolve().parents[1]

CSV_PATH = BASE / "data" / "ecommerce_orders.csv"
DATABASE_PATH = BASE / "data" / "ecommerce.db"


# --------------------------------------------------
# 1. Load CSV dataset
# --------------------------------------------------

df = pd.read_csv(
    CSV_PATH,
    parse_dates=["order_date"]
)

print("CSV rows:", len(df))
print("CSV columns:", len(df.columns))


# SQLite works cleanly with ISO date strings
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")


# --------------------------------------------------
# 2. Create SQLite database
# --------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

df.to_sql(
    "orders",
    connection,
    if_exists="replace",
    index=False,
)


# --------------------------------------------------
# 3. Verify table
# --------------------------------------------------

cursor = connection.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM orders"
)

row_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(DISTINCT order_id) FROM orders"
)

unique_orders = cursor.fetchone()[0]


cursor.execute(
    "SELECT MIN(order_date), MAX(order_date) FROM orders"
)

min_date, max_date = cursor.fetchone()


print("\nDATABASE CREATED SUCCESSFULLY")
print("-" * 50)

print("Table: orders")
print("Rows:", row_count)
print("Unique orders:", unique_orders)
print("Date range:", min_date, "to", max_date)

print("\nDatabase saved:")
print(DATABASE_PATH)


connection.close()