import os
import sys

# Asegurar que la raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QHeaderView,
    QStatusBar,
    QMessageBox,
    QFrame,
)

# Importación de componentes locales
from src.gui.widgets.custom_charts import StockChartWidget

# Importación segura de la base de datos
try:
    from src.data.database import DatabaseManager
except ImportError:
    try:
        from data.database import DatabaseManager
    except ImportError:
        DatabaseManager = None


class MainWindow(QMainWindow):
    """
    Ventana Principal Avanzada PySide6/Qt para NexusTech Solutions (Módulo 6.3).
    Implementa QTableWidget, QSS Theme, Menús y Custom QPainter Widget.
    """

    def __init__(self):
        super().__init__()

        # Inicializar manejador de BD si existe
        if DatabaseManager:
            try:
                self.db = DatabaseManager()
            except Exception:
                self.db = None
        else:
            self.db = None

        self.setWindowTitle("NexusTech Solutions - Gestión de Inventario (PySide6)")
        self.resize(900, 650)
        self.setMinimumSize(800, 500)

        # Aplicar Hoja de Estilos QSS (Dark Theme Catppuccin)
        self._apply_qss_theme()

        # Construir Componentes de la Interfaz
        self._create_menu_bar()
        self._setup_ui()

        # Cargar datos de prueba o SQLite
        self.load_inventory_data()

    def _apply_qss_theme(self):
        """Aplica estilos globales QSS para la interfaz."""
        qss = """
            QMainWindow { background-color: #1E1E2E; }
            QWidget { color: #CDD6F4; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; }
            QFrame#Sidebar { background-color: #181825; border-right: 1px solid #313244; }
            QPushButton { background-color: #313244; color: #CDD6F4; border: 1px solid #45475A; border-radius: 6px; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #45475A; border-color: #89B4FA; }
            QPushButton#PrimaryBtn { background-color: #89B4FA; color: #11111B; border: none; }
            QPushButton#PrimaryBtn:hover { background-color: #B4BEFE; }
            QTableWidget { background-color: #181825; gridline-color: #313244; border: 1px solid #313244; border-radius: 6px; selection-background-color: #45475A; selection-color: #89B4FA; }
            QHeaderView::section { background-color: #313244; color: #89B4FA; padding: 6px; font-weight: bold; border: none; }
            QStatusBar { background-color: #11111B; color: #A6ADC8; }
        """
        self.setStyleSheet(qss)

    def _create_menu_bar(self):
        """Crea la barra de menú superior."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Archivo")

        exit_action = QAction("&Salir", self)
        exit_action.setStatusTip("Cerrar la aplicación")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("&Ayuda")
        about_action = QAction("&Acerca de NexusTech", self)
        about_action.triggered.connect(
            lambda: QMessageBox.information(
                self,
                "Acerca de",
                "NexusTech Solutions v1.0\nDesarrollado por Ing. Nayib de la Cruz Márquez",
            )
        )
        help_menu.addAction(about_action)

    def _setup_ui(self):
        """Inicializa el layout principal de la ventana."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR LATERAL ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        lbl_logo = QLabel("NexusClient")
        lbl_logo.setStyleSheet("font-size: 18px; font-weight: bold; color: #89B4FA;")
        sidebar_layout.addWidget(lbl_logo)

        sidebar_layout.addSpacing(20)

        btn_refresh = QPushButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self.load_inventory_data)
        sidebar_layout.addWidget(btn_refresh)

        btn_add_mock = QPushButton("➕ Item Demo")
        btn_add_mock.setObjectName("PrimaryBtn")
        btn_add_mock.clicked.connect(self._add_demo_item)
        sidebar_layout.addWidget(btn_add_mock)

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # --- CONTENIDO PRINCIPAL ---
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Encabezado
        lbl_header = QLabel("Gestión de Inventario (PySide6 / QTableWidget)")
        lbl_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #CDD6F4;")
        content_layout.addWidget(lbl_header)

        # Tabla de Inventario (QTableWidget)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "SKU", "Nombre", "Stock", "Precio ($)"])

        # Modo de ajuste de encabezados para PySide6
        header = self.table.horizontalHeader()
        if hasattr(QHeaderView, "ResizeMode"):
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        else:
            header.setSectionResizeMode(QHeaderView.Stretch)

        content_layout.addWidget(self.table)

        # Widget Personalizado con QPainter (Entregable 6.3)
        self.chart_widget = StockChartWidget()
        content_layout.addWidget(self.chart_widget)

        main_layout.addWidget(content_area)

        # Barra de Estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo | Interfaz PySide6 cargada correctamente.")

    def load_inventory_data(self):
        """Obtiene datos desde SQLite o genera datos demo si no hay conexión."""
        products = []

        if self.db and hasattr(self.db, "get_all_products"):
            try:
                products = self.db.get_all_products()
            except Exception:
                products = []

        # Si no hay datos en la BD todavía, cargar lista inicial demo
        if not products:
            products = [
                {"id": 1, "sku": "NET-001", "name": "Servidor Rack 2U", "stock": 14, "price": 2500.00},
                {"id": 2, "sku": "NET-002", "name": "Switch Gigabit 24p", "stock": 42, "price": 380.50},
                {"id": 3, "sku": "NET-003", "name": "Router Balanceador", "stock": 8, "price": 890.00},
            ]

        self.table.setRowCount(len(products))

        total_stock = 0
        for row, prod in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(prod["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(prod["sku"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(prod["name"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(prod["stock"])))
            self.table.setItem(row, 4, QTableWidgetItem(f"${prod['price']:.2f}"))
            total_stock += prod["stock"]

        # Actualizar el Widget de QPainter con la capacidad
        calculated_level = min(100, int((total_stock / 150.0) * 100))
        self.chart_widget.set_stock_level(calculated_level if calculated_level > 0 else 45)

        self.status_bar.showMessage(f"Tabla actualizada: {len(products)} registros cargados.")

    def _add_demo_item(self):
        """Inserta un registro dinámico en la tabla."""
        import random
        num = random.randint(100, 999)
        if self.db and hasattr(self.db, "create_product"):
            try:
                self.db.create_product(f"SKU-{num}", f"Equipo Switch-{num}", "Redes", random.randint(1, 20), 450.00)
            except Exception:
                pass
        self.load_inventory_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())