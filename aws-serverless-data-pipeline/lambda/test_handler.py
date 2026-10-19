from handler import clean_rows


def test_clean_rows():
    raw = [
        {"order_id": "1", "order_date": "2025-01-05", "customer_name": " aarav patil ", "city": "PUNE",
         "product": "Laptop", "category": "Electronics", "quantity": "2", "unit_price": "55000"},
        {"order_id": "1", "order_date": "2025-01-05", "customer_name": "dup", "city": "Pune",
         "product": "Laptop", "category": "Electronics", "quantity": "2", "unit_price": "55000"},
        {"order_id": "2", "order_date": "31/02/2025", "customer_name": "x", "city": "Pune",
         "product": "Pen", "category": "Stationery", "quantity": "1", "unit_price": "10"},
        {"order_id": "3", "order_date": "2025-02-01", "customer_name": "y", "city": "Pune",
         "product": "Pen", "category": "Stationery", "quantity": "-1", "unit_price": "10"},
    ]
    clean, stats = clean_rows(raw)
    assert len(clean) == 1
    assert clean[0]["customer_name"] == "Aarav Patil"
    assert clean[0]["city"] == "Pune"
    assert clean[0]["total_amount"] == 110000.0
    assert stats == {"input": 4, "duplicates": 1, "invalid": 2}
