import os
import sys

# Asegurar que la raíz del proyecto esté agregada al PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """Punto de entrada principal para lanzar la app NexusTech Solutions."""
    app = QApplication(sys.argv)
    app.setApplicationName("NexusTech Solutions")

    # Instanciar y mostrar la ventana principal
    window = MainWindow()
    window.show()

    # Iniciar el bucle de eventos de la aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()