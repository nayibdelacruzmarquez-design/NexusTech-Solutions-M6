from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PySide6.QtWidgets import QWidget


class StockChartWidget(QWidget):
    """
    Widget personalizado que utiliza QPainter para renderizar
    un gráfico de barras / nivel de salud del inventario sin librerías externas.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self._stock_level = 75  # Porcentaje inicial por defecto (0 - 100)

    def set_stock_level(self, level: int):
        """Actualiza el nivel de stock y redibuja el widget."""
        self._stock_level = max(0, min(100, level))
        self.update()  # Fuerza la llamada a paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensiones del canvas
        width = self.width()
        height = self.height()

        # Dibujar Fondo del Card Widget
        rect_bg = QRectF(0, 0, width, height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#11111B")))
        painter.drawRoundedRect(rect_bg, 8, 8)

        # Dibujar Título del Widget
        painter.setPen(QPen(QColor("#89B4FA")))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(15, 25, "Métrica Visual: Capacidad de Inventario Local")

        # Dibujar Barra de Contención Externa
        bar_x, bar_y = 15, 45
        bar_w = width - 30
        bar_h = 30

        rect_bar_bg = QRectF(bar_x, bar_y, bar_w, bar_h)
        painter.setBrush(QBrush(QColor("#313244")))
        painter.drawRoundedRect(rect_bar_bg, 5, 5)

        # Determinar Color de Relleno según el Porcentaje
        if self._stock_level < 25:
            fill_color = QColor("#F38BA8")  # Rojo Crítico
        elif self._stock_level < 60:
            fill_color = QColor("#FAB387")  # Naranja Medio
        else:
            fill_color = QColor("#A6E3A1")  # Verde Óptimo

        # Dibujar Relleno Dinámico de la Barra
        fill_w = (bar_w * self._stock_level) / 100.0
        if fill_w > 0:
            rect_fill = QRectF(bar_x, bar_y, fill_w, bar_h)
            painter.setBrush(QBrush(fill_color))
            painter.drawRoundedRect(rect_fill, 5, 5)

        # Dibujar Porcentaje de Texto Centrado en la Barra
        painter.setPen(QPen(QColor("#11111B" if self._stock_level > 40 else "#FFFFFF")))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(
            QRectF(bar_x, bar_y, bar_w, bar_h),
            Qt.AlignCenter,
            f"{self._stock_level}% de Ocupación Utilizada",
        )

        # Leyenda inferior
        painter.setPen(QPen(QColor("#A6ADC8")))
        painter.setFont(QFont("Arial", 8))
        painter.drawText(
            15, height - 12, "Dibujado dinámicamente con QPainter (Modulo 6.3)"
        )