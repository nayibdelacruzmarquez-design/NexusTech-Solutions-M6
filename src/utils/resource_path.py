import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta hacia un recurso estático.
    Funciona tanto en modo desarrollo como dentro del ejecutable empaquetado por PyInstaller (_MEIPASS).
    """
    try:
        # PyInstaller crea una carpeta temporal _MEIPASS al ejecutar el .exe
        base_path = sys._MEIPASS
    except Exception:
        # En ejecución normal de Python, usa la raíz del proyecto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    return os.path.join(base_path, relative_path)