import time
from datetime import datetime
from PySide6.QtCore import QThread, Signal


class SyncWorkerThread(QThread):
    """
    Hilo secundario (QThread) para tareas pesadas en segundo plano (Módulo 6.5).
    Garantiza que la UI no se congele durante procesos síncronos o consumo de APIs.
    """

    progress_changed = Signal(int)  # Envía porcentaje (0-100)
    log_emitted = Signal(str)  # Envía log con timestamp
    sync_finished = Signal(bool, str)  # Envía estado final (éxito, mensaje)

    def __init__(self, items_to_process: int = 5, parent=None):
        super().__init__(parent)
        self.items_to_process = items_to_process
        self._is_running = True

    def run(self):
        """Ejecución del hilo en segundo plano."""
        try:
            self.log_emitted.emit(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [THREAD] Iniciando sincronización asíncrona...")

            for i in range(1, self.items_to_process + 1):
                if not self._is_running:
                    self.log_emitted.emit(
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [THREAD] Proceso cancelado.")
                    return

                # Simulación de carga/latencia (1 segundo por bloque)
                time.sleep(1.0)

                percentage = int((i / self.items_to_process) * 100)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                self.progress_changed.emit(percentage)
                self.log_emitted.emit(
                    f"[{timestamp}] [THREAD] Lote {i}/{self.items_to_process} procesado ({percentage}%)")

            self.sync_finished.emit(True, "Sincronización masiva completada.")
            self.log_emitted.emit(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [THREAD] Hilo secundario finalizado con éxito.")

        except Exception as e:
            self.sync_finished.emit(False, f"Error en el hilo: {str(e)}")

    def stop(self):
        self._is_running = False