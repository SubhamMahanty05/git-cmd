# StockPulse — Supply Chain Demand & Inventory Intelligence

**Portfolio project | Synthetic demonstration data | Python + SQL + Power BI**

StockPulse demonstrates an end-to-end supply-chain analytics workflow: historical sales analysis, a 30-day demand forecast baseline, inventory risk classification, replenishment recommendations, SQL business queries and a Power BI dashboard specification.

## Project scope
- 54,750 daily sales records generated across 30 products and five warehouses (365 days).
- Python analysis with Pandas and NumPy.
- 30-day demand forecast using a 28-day moving-average baseline with damped trend.
- Inventory classification: Stockout, Reorder Risk, Healthy and Excess Stock.
- Replenishment quantity based on lead-time demand plus three safety-stock days.
- Ten SQL business queries.
- Power BI dashboard plan and DAX KPI measures.

## Quick start (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/generate_data.py
python src/analyze.py
python src/forecast.py
python src/inventory_analysis.py
```

## Power BI
Follow powerbi/POWER_BI_GUIDE.md. Import the generated CSVs, create relationships, add measures from powerbi/DAX_measures.txt, build three dashboard pages and save the native report as powerbi/StockPulse.pbix.

## CV description — use after completing the Power BI dashboard
Developed StockPulse, a supply-chain analytics project using Python and SQL to analyse historical product demand, generate a 30-day forecast baseline, identify stockout and excess-inventory risks, and calculate replenishment recommendations. Built Power BI dashboards with DAX KPIs for product- and warehouse-level monitoring.

Only claim the Power BI dashboard as completed after you have built and saved the PBIX file.

## Limitations
All data is synthetic and is not actual HP or company data. The forecast is a simple, interpretable baseline rather than a tuned production forecasting system. Inventory thresholds are illustrative assumptions.
