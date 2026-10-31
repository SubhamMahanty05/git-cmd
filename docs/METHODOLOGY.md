# StockPulse methodology

## Data
All records are synthetic, generated for portfolio demonstration only. The generator simulates 365 days of demand for 30 products across five warehouses. Demand includes weekday effects, smooth annual seasonality, product and warehouse variation, and random Poisson noise.

## Forecast baseline
For each product-warehouse pair, use the mean of the most recent 28 days. Adjust the baseline using a damped recent-versus-prior 28-day trend clipped to +/-20%. This is a transparent baseline, not a tuned production model.

## Inventory rules
- Average daily demand: latest 30 days.
- Lead-time demand: average daily demand multiplied by supplier lead time.
- Safety stock: three days of average demand.
- Reorder point: lead-time demand plus safety stock.
- Recommended order: max(0, reorder point minus on-hand stock).
- Stockout: zero units on hand.
- Reorder Risk: on-hand stock below reorder point.
- Excess Stock: more than 60 days of coverage.
- Healthy: none of the above.

These thresholds are illustrative and must be calibrated with actual business policies before operational use.
