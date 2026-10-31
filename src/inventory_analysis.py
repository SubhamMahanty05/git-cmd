"""Calculate days of inventory, reorder points and stock risk."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sales = pd.read_csv(ROOT/"data/raw/sales.csv", parse_dates=["date"])
products = pd.read_csv(ROOT/"data/raw/products.csv")
warehouses = pd.read_csv(ROOT/"data/raw/warehouses.csv")
inventory = pd.read_csv(ROOT/"data/raw/inventory.csv")
end = sales.date.max()
recent = (sales[sales.date >= end-pd.Timedelta(days=29)]
          .groupby(["product_id","warehouse_id"], as_index=False)
          .sales_quantity.mean().rename(columns={"sales_quantity":"avg_daily_demand_30d"}))
out = (inventory.merge(products, on="product_id")
       .merge(warehouses, on="warehouse_id")
       .merge(recent, on=["product_id","warehouse_id"], how="left"))
out["avg_daily_demand_30d"] = out.avg_daily_demand_30d.fillna(0)
out["days_of_inventory"] = np.where(out.avg_daily_demand_30d > 0,
    out.stock_quantity/out.avg_daily_demand_30d, np.nan)
out["lead_time_demand"] = out.avg_daily_demand_30d*out.lead_time_days
out["safety_stock"] = out.avg_daily_demand_30d*3
out["reorder_point"] = out.lead_time_demand+out.safety_stock
out["recommended_order_qty"] = np.maximum(0, np.ceil(out.reorder_point-out.stock_quantity)).astype(int)
out["stock_status"] = np.select([
    out.stock_quantity == 0,
    out.stock_quantity < out.reorder_point,
    out.days_of_inventory > 60
], ["Stockout","Reorder Risk","Excess Stock"], default="Healthy")
out["inventory_value"] = out.stock_quantity*out.unit_price
target = ROOT/"data/processed"
target.mkdir(parents=True, exist_ok=True)
out.to_csv(target/"inventory_analysis.csv", index=False)
print("Saved inventory risk analysis for", len(out), "product-warehouse combinations.")
