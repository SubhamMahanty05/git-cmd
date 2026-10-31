-- Monthly demand and revenue
SELECT substr(date,1,7) AS month, SUM(sales_quantity) AS units, SUM(sales_revenue) AS revenue
FROM sales GROUP BY substr(date,1,7) ORDER BY month;

-- Revenue by product category
SELECT p.category, SUM(s.sales_revenue) AS revenue
FROM sales s JOIN products p USING(product_id)
GROUP BY p.category ORDER BY revenue DESC;

-- Warehouse performance
SELECT w.warehouse_name, SUM(s.sales_quantity) AS units, SUM(s.sales_revenue) AS revenue
FROM sales s JOIN warehouses w USING(warehouse_id)
GROUP BY w.warehouse_name ORDER BY revenue DESC;

-- Replenishment candidates
SELECT product_id, product_name, warehouse_name, stock_quantity, reorder_point,
       recommended_order_qty, stock_status
FROM inventory_analysis WHERE stock_status IN ('Stockout','Reorder Risk')
ORDER BY recommended_order_qty DESC;

-- Excess inventory exposure
SELECT product_id, product_name, warehouse_name, days_of_inventory, inventory_value
FROM inventory_analysis WHERE stock_status='Excess Stock' ORDER BY inventory_value DESC;

-- Inventory risk summary
SELECT stock_status, COUNT(*) AS combinations, SUM(stock_quantity) AS units_on_hand,
       SUM(inventory_value) AS inventory_value
FROM inventory_analysis GROUP BY stock_status;

-- Top 10 products by revenue
SELECT p.product_name, SUM(s.sales_quantity) AS units, SUM(s.sales_revenue) AS revenue
FROM sales s JOIN products p USING(product_id)
GROUP BY p.product_id, p.product_name ORDER BY revenue DESC LIMIT 10;

-- 30-day forecast totals
SELECT product_id, ROUND(SUM(forecast_demand),0) AS forecast_units
FROM demand_forecast GROUP BY product_id ORDER BY forecast_units DESC;

-- Stock coverage for non-healthy combinations
SELECT product_id, product_name, warehouse_name, days_of_inventory, lead_time_days, stock_status
FROM inventory_analysis WHERE stock_status <> 'Healthy' ORDER BY days_of_inventory;

-- Monthly category demand
SELECT m.month, p.category, SUM(m.sales_quantity) AS units
FROM monthly_sales m JOIN products p USING(product_id)
GROUP BY m.month, p.category ORDER BY m.month, p.category;
