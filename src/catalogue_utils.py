
import pandas as pd

def validate_catalogue(products):
    """Check that the product catalogue contains valid data."""

    required_columns = [
        "product_id",
        "name",
        "category",
        "description",
        "price_ghs",
        "stock_qty"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in products.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    if products.empty:
        raise ValueError("The product catalogue is empty.")

    products = products.copy()

    products["price_ghs"] = pd.to_numeric(
        products["price_ghs"], errors="coerce"
    )

    products["stock_qty"] = pd.to_numeric(
        products["stock_qty"], errors="coerce"
    )

    if products["price_ghs"].isna().any() or (
        products["price_ghs"] < 0
    ).any():
        raise ValueError(
            "Prices must be valid, non-negative numbers."
        )

    if (
        products["stock_qty"].isna().any()
        or (products["stock_qty"] < 0).any()
        or (products["stock_qty"] % 1 != 0).any()
    ):
        raise ValueError(
            "Stock quantities must be non-negative whole numbers."
        )

    return products
