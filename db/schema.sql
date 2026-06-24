CREATE TABLE companies (
    id INTEGER,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

CREATE TABLE profitandloss (
    id INTEGER PRIMARY KEY
);

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY
);

CREATE TABLE cashflow (
    id INTEGER PRIMARY KEY
);

CREATE TABLE analysis (
    id INTEGER PRIMARY KEY
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY
);

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY
);

CREATE TABLE sectors (
    id INTEGER,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT
);

CREATE TABLE financial_ratios (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    debt_to_equity REAL
);

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY
);

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY
);