import unittest
from src.data.api_client import InventoryApiClient


class TestApiClient(unittest.TestCase):
    def setUp(self):
        self.api_client = InventoryApiClient()

    def test_fetch_products_structure(self):
        # Desempaquetamos la tupla (productos, es_cache, mensaje) que retorna el método
        products, is_cache, msg = self.api_client.fetch_external_products()

        # Validamos que la primera posición sea efectivamente una lista
        self.assertIsInstance(products, list)
        self.assertIsInstance(is_cache, bool)
        self.assertIsInstance(msg, str)

        # Si hay elementos, validamos la estructura normalizada de la API
        if len(products) > 0:
            first_item = products[0]
            self.assertIn("sku", first_item)
            self.assertIn("name", first_item)
            self.assertIn("price", first_item)


if __name__ == "__main__":
    unittest.main()