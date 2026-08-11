# NexusTech Solutions - M6
Aplicación modular de escritorio desarrollada en Python con **PySide6**, persistencia en **SQLite**, resiliencia offline ante fallos de API REST, ejecución multihilo asíncrona y dashboard web con **PyScript (WebAssembly)**.

---

## Requisitos Previos

* **Python:** v3.12 o superior
* **Sistema Operativo:** Windows 10/11, macOS o Linux
* **IDE Recomendado:** PyCharm

---

## Instalación y Configuración del Entorno

1. **Clonar o descomprimir el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd NexusTech_Solutions_M6_DeLaCruzNayib
   ```
   
 2. Crear y activar el entorno virtual:
   ```PowerShell
   python -m venv .venv
    .\.venv\Scripts\activate
   ```
3. Instalar dependencias
   ```bash
    pip install -r requirements.txt
   ```
## Ejecución de la Aplicación
1. Aplicación de Escritorio (PySide6)
Para iniciar la interfaz gráfica nativa desde el código fuente:
   ```bash
    python src/main.py
   ```
2. Ejecutar el Binario Compilado (.exe)
Puedes ejecutar la aplicación directamente sin necesidad de Python:
* Navega a la carpeta dist/ y ejecuta NexusTech_Solutions.exe.
3. Dashboard Web (PyScript)
Para ejecutar la lógica Python en el navegador:
* Abre la carpeta pyscript/.

* Abre el archivo index.html en Chrome o Edge.

* Haz clic en ⚡ Cargar Datos desde API (Python) para ejecutar la petición asíncrona WASM.

## Pruebas Unitarias
Para verificar la creación de tablas y la integridad de SQLite:
   ```bash
    python -m unittest tests/test_database.py
   ```

## Archivos de Evidencia (Sección 8)
* git_log.txt: Historial de commits del desarrollo iterativo.

* pyinstaller_build_log.txt: Log crudo del empaquetado del ejecutable.

* docs/screenshots/: Capturas de pantalla de la app en modo Online, Offline/Resiliencia, Executable y PyScript Web.
* 