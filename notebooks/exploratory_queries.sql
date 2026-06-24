SELECT COUNT(*) FROM companies;

SELECT COUNT(*) FROM stock_prices;

SELECT COUNT(*) FROM financial_ratios;

SELECT *
FROM companies
LIMIT 10;

SELECT *
FROM financial_ratios
LIMIT 10;

SELECT company_id,
AVG(return_on_equity_pct)
FROM financial_ratios
GROUP BY company_id;

SELECT broad_sector,
COUNT(*)
FROM sectors
GROUP BY broad_sector;

SELECT company_id,
MAX(return_on_equity_pct)
FROM financial_ratios
GROUP BY company_id;

SELECT company_id,
AVG(net_profit_margin_pct)
FROM financial_ratios
GROUP BY company_id;

SELECT *
FROM stock_prices
LIMIT 20;