"""Exploratory business analysis for StockPulse."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sales = pd.read_csv(ROOT/"data/raw/sales.csv", parse_dates=["date"])
products = pd.read_csv(ROOT/"data/raw/products.csv")
print("Date range:", sales.date.min().date(), "to", sales.date.max().date())
print("Sales records:", f"{len(sales):,}")
print("Total units:", f"{sales.sales_quantity.sum():,}")
print("Revenue:", f"{sales.sales_revenue.sum():,.2f}")
print("\nRevenue by category:")
print(sales.merge(products[["product_id","category"]], on="product_id")
      .groupby("category").sales_revenue.sum().sort_values(ascending=False))
print("\nMonthly demand:")
print(sales.groupby("month").sales_quantity.sum())
