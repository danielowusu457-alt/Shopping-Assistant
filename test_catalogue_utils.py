
import unittest
import pandas as pd

from src.catalogue_utils import validate_catalogue


class TestCatalogueValidation(unittest.TestCase):

    def setUp(self):
        self.valid_products = pd.DataFrame({
            "product_id": ["P001"],
            "name": ["Headphones"],
            "category": ["Electronics"],
            "description": ["Wireless headphones"],
            "price_ghs": [200],
            "stock_qty": [10]
        })

    def test_valid_catalogue(self):
        result = validate_catalogue(self.valid_products)
        self.assertEqual(len(result), 1)

    def test_missing_column(self):
        products = self.valid_products.drop(columns=["name"])

        with self.assertRaises(ValueError):
            validate_catalogue(products)

    def test_invalid_price(self):
        products = self.valid_products.copy()
        products["price_ghs"] = ["ABC"]

        with self.assertRaises(ValueError):
            validate_catalogue(products)

    def test_negative_price(self):
        products = self.valid_products.copy()
        products["price_ghs"] = [-100]

        with self.assertRaises(ValueError):
            validate_catalogue(products)

    def test_invalid_stock(self):
        products = self.valid_products.copy()
        products["stock_qty"] = ["ABC"]

        with self.assertRaises(ValueError):
            validate_catalogue(products)

    def test_empty_catalogue(self):
        products = self.valid_products.iloc[0:0]

        with self.assertRaises(ValueError):
            validate_catalogue(products)


if __name__ == "__main__":
    unittest.main()
