-- Star schema: one fact table surrounded by dimension tables
CREATE TABLE dim_customer (
    customer_key  INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city          TEXT NOT NULL
);

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product     TEXT NOT NULL,
    category    TEXT NOT NULL
);

CREATE TABLE dim_date (
    date_key    INTEGER PRIMARY KEY,   -- YYYYMMDD
    full_date   TEXT NOT NULL,
    year        INTEGER,
    month       INTEGER,
    month_name  TEXT,
    quarter     INTEGER,
    day_of_week TEXT
);

CREATE TABLE fact_sales (
    order_id     INTEGER PRIMARY KEY,
    date_key     INTEGER NOT NULL REFERENCES dim_date(date_key),
    customer_key INTEGER NOT NULL REFERENCES dim_customer(customer_key),
    product_key  INTEGER NOT NULL REFERENCES dim_product(product_key),
    quantity     INTEGER NOT NULL,
    unit_price   REAL NOT NULL,
    total_amount REAL NOT NULL
);

CREATE INDEX idx_fact_date     ON fact_sales(date_key);
CREATE INDEX idx_fact_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_product  ON fact_sales(product_key);
