"""AWS Lambda: triggered when a raw CSV lands in s3://<bucket>/raw/.
Cleans the data (pure Python, no extra layers needed) and writes it to s3://<bucket>/clean/
so Amazon Athena can query it."""
import csv
import io
import logging
import os
import urllib.parse
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OUT_FIELDS = ["order_id", "order_date", "customer_name", "city",
              "product", "category", "quantity", "unit_price", "total_amount"]


def clean_rows(rows):
    """Pure function (easy to unit-test): returns (clean_rows, stats)."""
    seen, clean = set(), []
    stats = {"input": 0, "duplicates": 0, "invalid": 0}
    for r in rows:
        stats["input"] += 1
        oid = (r.get("order_id") or "").strip()
        if oid in seen:
            stats["duplicates"] += 1
            continue
        seen.add(oid)
        try:
            date = datetime.strptime(r["order_date"].strip(), "%Y-%m-%d").date().isoformat()
            qty = int(float(r["quantity"]))
            price = float(r["unit_price"])
            if qty <= 0 or price <= 0:
                raise ValueError("non-positive quantity/price")
        except (ValueError, KeyError, TypeError):
            stats["invalid"] += 1
            continue
        clean.append({
            "order_id": oid,
            "order_date": date,
            "customer_name": r["customer_name"].strip().title(),
            "city": (r.get("city") or "Unknown").strip().title() or "Unknown",
            "product": r["product"].strip(),
            "category": r["category"].strip(),
            "quantity": qty,
            "unit_price": price,
            "total_amount": round(qty * price, 2),
        })
    return clean, stats


def lambda_handler(event, context):
    import boto3  # imported here so clean_rows can be tested without AWS libs
    s3 = boto3.client("s3")

    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["object"]["key"])
    logger.info("Processing s3://%s/%s", bucket, key)

    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")
    clean, stats = clean_rows(csv.DictReader(io.StringIO(body)))

    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=OUT_FIELDS)
    writer.writeheader()          # Athena table below skips this header row
    writer.writerows(clean)

    out_key = os.environ.get("CLEAN_PREFIX", "clean/") + os.path.basename(key)
    s3.put_object(Bucket=bucket, Key=out_key, Body=out.getvalue().encode("utf-8"))
    logger.info("Wrote %d clean rows to s3://%s/%s | stats=%s", len(clean), bucket, out_key, stats)
    return {"statusCode": 200, "clean_rows": len(clean), **stats}
