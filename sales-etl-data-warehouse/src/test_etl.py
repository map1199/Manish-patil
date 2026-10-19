"""Basic data-quality tests. Run with:  pytest -q"""
from etl import transform
from generate_data import build


def test_no_duplicates_and_valid_values():
    clean = transform(build())
    assert clean["order_id"].is_unique
    assert (clean["quantity"] > 0).all()
    assert clean["unit_price"].notna().all()
    assert clean["order_date"].notna().all()
    assert (clean["city"] == clean["city"].str.title()).all()


def test_total_amount_is_correct():
    clean = transform(build())
    assert (clean["total_amount"] == clean["quantity"] * clean["unit_price"]).all()
