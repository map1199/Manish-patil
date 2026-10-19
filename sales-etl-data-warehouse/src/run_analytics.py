"""Run every query in sql/analytics.sql and print the results."""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
conn = sqlite3.connect(ROOT / "data" / "warehouse.db")
queries = [q.strip() for q in (ROOT / "sql" / "analytics.sql").read_text().split(";") if "SELECT" in q]

for q in queries:
    title = q.splitlines()[0].lstrip("- ").strip()
    print(f"\n=== {title} ===")
    print(pd.read_sql_query(q, conn).to_string(index=False))
conn.close()
