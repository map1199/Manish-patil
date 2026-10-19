"""Generate a messy raw sales CSV so the ETL pipeline has realistic problems to fix
(duplicates, missing values, inconsistent text, bad dates, negative quantities)."""
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)

PRODUCTS = {
    "Laptop": ("Electronics", 55000), "Smartphone": ("Electronics", 22000),
    "Headphones": ("Electronics", 2500), "Office Chair": ("Furniture", 7500),
    "Desk": ("Furniture", 9500), "Notebook": ("Stationery", 120),
    "Pen Pack": ("Stationery", 80), "Backpack": ("Accessories", 1800),
}
CITIES = ["Pune", "Mumbai", "Nagpur", "Nashik", "Nanded", "Aurangabad"]
FIRST = ["Aarav", "Riya", "Sneha", "Rohan", "Isha", "Karan", "Neha", "Omkar", "Pooja", "Yash"]
LAST = ["Patil", "Deshmukh", "Joshi", "Kulkarni", "More", "Jadhav", "Shinde", "Pawar"]


def build(rows: int = 1500) -> pd.DataFrame:
    start = date(2025, 1, 1)
    data = []
    for i in range(1, rows + 1):
        product = random.choice(list(PRODUCTS))
        category, price = PRODUCTS[product]
        data.append({
            "order_id": 1000 + i,
            "order_date": (start + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d"),
            "customer_name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "city": random.choice(CITIES),
            "product": product,
            "category": category,
            "quantity": random.randint(1, 5),
            "unit_price": price,
        })
    df = pd.DataFrame(data)

    # --- inject data-quality problems ---
    df = pd.concat([df, df.sample(40, random_state=1)]).reset_index(drop=True)  # duplicates
    df.loc[df.sample(30, random_state=2).index, "city"] = None                  # missing city
    idx = df.sample(30, random_state=3).index
    df.loc[idx, "city"] = df.loc[idx, "city"].str.upper()                       # inconsistent case
    idx = df.sample(20, random_state=4).index
    df.loc[idx, "customer_name"] = "  " + df.loc[idx, "customer_name"] + "  "   # stray spaces
    df.loc[df.sample(15, random_state=5).index, "quantity"] = -1                # invalid quantity
    df.loc[df.sample(15, random_state=6).index, "order_date"] = "31/02/2025"    # impossible date
    df.loc[df.sample(10, random_state=7).index, "unit_price"] = None            # missing price
    return df.sample(frac=1, random_state=9).reset_index(drop=True)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "data" / "raw_sales.csv"
    out.parent.mkdir(exist_ok=True)
    build().to_csv(out, index=False)
    print(f"Raw data written to {out}")
