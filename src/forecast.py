"""30-day demand baseline: 28-day moving average with damped trend."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
daily = pd.read_csv(ROOT/"data/raw/sales.csv", parse_dates=["date"])
daily = daily.groupby(["date","product_id","warehouse_id"], as_index=False).sales_quantity.sum()
cutoff = daily.date.max()
rows = []
for (product, warehouse), group in daily.groupby(["product_id","warehouse_id"]):
    group = group.sort_values("date")
    recent = group.tail(28).sales_quantity.mean()
    previous = group.iloc[-56:-28].sales_quantity.mean()
    trend = np.clip((recent-previous)/max(previous,1), -.20, .20)
    for horizon in range(1,31):
        prediction = max(0, recent*(1 + trend*min(horizon/30,1)*.5))
        rows.append((cutoff+pd.Timedelta(days=horizon), product, warehouse, round(prediction,2)))
out = pd.DataFrame(rows, columns=["forecast_date","product_id","warehouse_id","forecast_demand"])
target = ROOT/"data/processed"
target.mkdir(parents=True, exist_ok=True)
out.to_csv(target/"demand_forecast_30d.csv", index=False)
print("Saved", len(out), "forecast rows.")
