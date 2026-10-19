"""ETL pipeline: raw CSV -> cleaned data -> SQLite star-schema warehouse."""
import logging
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = ROOT / "data" / "raw_sales.csv"
DB_FILE = ROOT / "data" / "warehouse.db"
SCHEMA_FILE = ROOT / "sql" / "schema.sql"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("etl")


# ------------------------------------------------------------------ EXTRACT
def extract(path: Path = RAW_FILE) -> pd.DataFrame:
    df = pd.read_csv(path)
    log.info("Extracted %d raw rows", len(df))
    return df


# ---------------------------------------------------------------- TRANSFORM
def transform(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset="order_id").copy()
    log.info("Removed %d duplicate orders", before - len(df))

    df["customer_name"] = df["customer_name"].str.strip().str.title()
    df["city"] = df["city"].str.strip().str.title().fillna("Unknown")

    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # fill missing prices using the median price of the same product
    df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))

    bad = df["order_date"].isna() | (df["quantity"] <= 0) | df["unit_price"].isna()
    log.info("Dropped %d rows with invalid date / quantity / price", bad.sum())
    df = df[~bad].copy()

    df["total_amount"] = df["quantity"] * df["unit_price"]
    log.info("Transformed data: %d clean rows", len(df))
    return df


# --------------------------------------------------------------------- LOAD
def load(df: pd.DataFrame, db_file: Path = DB_FILE) -> None:
    if db_file.exists():
        db_file.unlink()                       # full refresh for the demo
    conn = sqlite3.connect(db_file)
    conn.executescript(SCHEMA_FILE.read_text())

    dim_customer = df[["customer_name", "city"]].drop_duplicates().reset_index(drop=True)
    dim_customer.insert(0, "customer_key", dim_customer.index + 1)

    dim_product = df[["product", "category"]].drop_duplicates().reset_index(drop=True)
    dim_product.insert(0, "product_key", dim_product.index + 1)

    dates = pd.DataFrame({"full_date": pd.to_datetime(sorted(df["order_date"].unique()))})
    dates["date_key"] = dates["full_date"].dt.strftime("%Y%m%d").astype(int)
    dates["year"] = dates["full_date"].dt.year
    dates["month"] = dates["full_date"].dt.month
    dates["month_name"] = dates["full_date"].dt.strftime("%B")
    dates["quarter"] = dates["full_date"].dt.quarter
    dates["day_of_week"] = dates["full_date"].dt.day_name()
    dates["full_date"] = dates["full_date"].dt.strftime("%Y-%m-%d")

    fact = (
        df.merge(dim_customer, on=["customer_name", "city"])
          .merge(dim_product, on=["product", "category"])
    )
    fact["date_key"] = fact["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact = fact[["order_id", "date_key", "customer_key", "product_key",
                 "quantity", "unit_price", "total_amount"]]

    dim_customer.to_sql("dim_customer", conn, if_exists="append", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="append", index=False)
    dates.to_sql("dim_date", conn, if_exists="append", index=False)
    fact.to_sql("fact_sales", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    log.info("Loaded warehouse: %d customers, %d products, %d dates, %d sales",
             len(dim_customer), len(dim_product), len(dates), len(fact))


def run() -> None:
    load(transform(extract()))


if __name__ == "__main__":
    run()
