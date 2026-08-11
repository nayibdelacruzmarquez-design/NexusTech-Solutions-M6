import time
from datetime import datetime
from PySide6.QtCore import QThread, Signal
# Importación corregida apuntando a la capa src.data
from src.data.api_client import InventoryApiClient
from src.data.database import DatabaseManager


class SyncWorkerThread(QThread):
    """
    Hilo secundario (QThread) para ejecutar el consumo de la API
    y el guardado en SQLite sin congelar la UI.
    """

    progress_changed = Signal(int)
    log_emitted = Signal(str)
    sync_finished = Signal(bool, str)

    def __init__(self, items_to_process=5, parent=None):
        super().__init__(parent)
        self.items_to_process = items_to_process
        self.db = DatabaseManager()
        self.api_client = InventoryApiClient(self.db)

    def run(self):
        try:
            self.log_emitted.emit(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [THREAD] Conectando con API externa REST..."
            )
            self.progress_changed.emit(20)
            time.sleep(0.5)

            # Consumo de API REST + Resiliencia / Caché
            products, is_cache, msg = self.api_client.fetch_external_products()
            self.progress_changed.emit(60)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_emitted.emit(f"[{timestamp}] [API] {msg}")

            if products:
                for prod in products:
                    try:
                        self.db.create_product(
                            prod["sku"], prod["name"], prod["category"], prod["stock"], prod["price"]
                        )
                    except Exception:
                        pass  # Evita errores si el SKU ya existe

                self.progress_changed.emit(100)
                self.log_emitted.emit(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [DB] Registros guardados exitosamente en SQLite."
                )
                self.sync_finished.emit(
                    True, f"Sincronización finalizada. {'(Desde Caché)' if is_cache else '(Online)'}"
                )
            else:
                self.sync_finished.emit(False, "No se pudieron obtener datos.")

        except Exception as e:
            self.sync_finished.emit(False, f"Error en hilo de sincronización: {str(e)}")