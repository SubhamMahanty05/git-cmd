# Power BI Desktop dashboard guide

## Import data
Run the Python generation scripts first. Import these CSVs using Home > Get Data > Text/CSV:
- data/raw/sales.csv
- data/raw/products.csv
- data/raw/warehouses.csv
- data/processed/inventory_analysis.csv
- data/processed/demand_forecast_30d.csv

## Model relationships
Create one-to-many, single-direction relationships from products[product_id] and warehouses[warehouse_id] to matching keys in sales, inventory_analysis and demand_forecast_30d. Keep inventory_analysis as a separate inventory snapshot table. Avoid ambiguous bidirectional relationships.

## DAX
Create measures from DAX_measures.txt using Modeling > New measure.

## Page 1 — Executive Overview
KPI cards: Total Revenue, Total Units Sold, Current Stock Units, Products at Reorder Risk, Forecast Demand 30D.
Charts: daily sales line chart, revenue by category, revenue by warehouse.
Slicers: category, warehouse and date.

## Page 2 — Demand Forecast
Line chart: forecast_demand by forecast_date.
Table: product_id, warehouse_id, forecast_demand.
For a combined actual-vs-forecast chart, create a shared Date table and relate it to sales[date] and demand_forecast_30d[forecast_date].

## Page 3 — Inventory Intelligence
Cards: Inventory Value, Recommended Replenishment Units, Excess Stock Units.
Donut: product-warehouse combination count by stock_status.
Table: product, warehouse, stock_quantity, days_of_inventory, reorder_point, recommended_order_qty, stock_status.
Add conditional formatting and category/warehouse/status slicers.

Save the native report as powerbi/StockPulse.pbix. This repository provides the prepared data and dashboard instructions; a PBIX must be created in Power BI Desktop.
