import json
import urllib.request
import urllib.error
from typing import Tuple, List, Dict, Any, Optional
from src.data.database import DatabaseManager


class InventoryApiClient:
    """
    Cliente HTTP para consumir APIs RESTful externas (Módulo 6.6).
    Implementa resiliencia ante errores de red respaldándose en SQLite (Caché).
    """

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        # API de prueba pública segura
        self.api_url = "https://fakestoreapi.com/products?limit=5"
        self.db = db_manager or DatabaseManager()

    def fetch_external_products(self) -> Tuple[List[Dict[str, Any]], bool, str]:
        """
        Intenta obtener datos remotos de la API.
        En caso de fallo de red (Timeout/Sin internet), recupera los datos del caché de SQLite.
        """
        try:
            req = urllib.request.Request(
                self.api_url,
                headers={"User-Agent": "NexusTech-Client/1.0"}
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data_bytes = response.read()
                    data_str = data_bytes.decode('utf-8')
                    raw_products = json.loads(data_str)

                    # Guardar respuesta exitosa en la tabla api_cache de SQLite
                    self.db.save_cache(self.api_url, data_str)

                    parsed_products = self._normalize_data(raw_products)
                    return parsed_products, False, "Sincronización online exitosa (API REST)."

        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception) as err:
            # Resiliencia: Fallback al Caché Local almacenado en SQLite
            cached_data = self.db.get_cache(self.api_url)
            if cached_data:
                raw_products = json.loads(cached_data)
                parsed_products = self._normalize_data(raw_products)
                return parsed_products, True, f"Fallo de red ({type(err).__name__}). Datos recuperados desde Caché local."

            return [], True, f"Error crítico de red sin caché disponible: {str(err)}"

    def _normalize_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Mapea la respuesta de la API al esquema interno del sistema."""
        normalized = []
        for idx, item in enumerate(raw_data, 1):
            normalized.append({
                "sku": f"API-{item.get('id', idx):03d}",
                "name": str(item.get('title', 'Producto Remoto'))[:25],
                "category": str(item.get('category', 'Importado')),
                "stock": int(item.get('rating', {}).get('count', 10)),
                "price": float(item.get('price', 99.99))
            })
        return normalized