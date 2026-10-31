"""Generate reproducible synthetic retail supply-chain data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)
categories = ["Laptop"] * 8 + ["Desktop"] * 8 + ["Monitor"] * 8 + ["Accessory"] * 6
products = pd.DataFrame([{
    "product_id": f"P{i:03}", "product_name": f"{cat} Model {i:02}",
    "category": cat, "unit_price": int(rng.integers(80, 1800)),
    "lead_time_days": int(rng.integers(5, 26)),
    "supplier_id": f"S{int(rng.integers(1, 9)):03}"
} for i, cat in enumerate(categories, 1)])
warehouses = pd.DataFrame({
    "warehouse_id": ["W01", "W02", "W03", "W04", "W05"],
    "warehouse_name": ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Pune"],
    "region": ["North", "West", "South", "South", "West"]
})

dates = pd.date_range(end=pd.Timestamp.today().normalize() - pd.Timedelta(days=1), periods=365)
rows = []
for p in products.itertuples(index=False):
    base = rng.uniform(7, 30)
    for w in warehouses.itertuples(index=False):
        warehouse_factor, phase = rng.uniform(.65, 1.35), rng.uniform(0, 2*np.pi)
        for j, day in enumerate(dates):
            weekday = 1.25 if day.dayofweek in (4, 5) else (.85 if day.dayofweek == 0 else 1)
            season = 1 + .18*np.sin(2*np.pi*j/365 + phase)
            demand = base * warehouse_factor * weekday * season * (1 + .0005*j)
            qty = int(rng.poisson(max(0, demand)))
            rows.append((day, p.product_id, w.warehouse_id, qty, p.unit_price, qty*p.unit_price))
sales = pd.DataFrame(rows, columns=["date","product_id","warehouse_id","sales_quantity","unit_price","sales_revenue"])
sales["month"] = pd.to_datetime(sales["date"]).dt.to_period("M").astype(str)

stock_rows = []
for p in products.itertuples(index=False):
    for w in warehouses.itertuples(index=False):
        recent = sales[(sales.product_id == p.product_id) & (sales.warehouse_id == w.warehouse_id)].tail(30).sales_quantity.mean()
        stock = max(0, int(recent * rng.uniform(2, 75)))
        stock_rows.append((p.product_id, w.warehouse_id, stock, p.lead_time_days,
                           pd.Timestamp.today().normalize() - pd.Timedelta(days=int(rng.integers(0, 100)))))
inventory = pd.DataFrame(stock_rows, columns=["product_id","warehouse_id","stock_quantity","lead_time_days","last_restock_date"])

products.to_csv(RAW/"products.csv", index=False)
warehouses.to_csv(RAW/"warehouses.csv", index=False)
sales.to_csv(RAW/"sales.csv", index=False)
inventory.to_csv(RAW/"inventory.csv", index=False)
print(f"Generated {len(sales):,} sales rows, {len(products)} products and {len(warehouses)} warehouses.")
