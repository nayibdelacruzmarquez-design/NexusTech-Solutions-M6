from PySide6.QtCore import QObject, Signal


class AppSignals(QObject):
    """
    Bus de Señales Centralizado para NexusTech Solutions (Módulo 6.4).
    Permite la comunicación desacoplada entre la UI, hilos y la capa de datos.
    """

    # 1. Notificación de cambios en el inventario (Pasa dict con datos del producto)
    product_added = Signal(dict)
    product_updated = Signal(dict)
    product_deleted = Signal(int)

    # 2. Notificación de estado general del sistema (Pasa mensaje en str y nivel)
    status_changed = Signal(str, str)  # (mensaje, nivel: 'INFO', 'WARN', 'ERROR')

    # 3. Notificación de sincronización API / Hilos (Pasa progreso en int 0-100)
    sync_progress = Signal(int)
    sync_completed = Signal(bool, str)  # (éxito, mensaje_resultado)


# Instancia global del bus de señales (Singleton)
signals = AppSignals()