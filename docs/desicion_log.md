# Registro de Decisiones de Arquitectura (Decision Log) - NexusTech Solutions

## Módulo 6.1: Justificación de Arquitectura y Diseño de UI

### 1. Elección del Patrón de Arquitectura: MVC / MVVM Desacoplado
Se ha seleccionado un enfoque orientado a eventos combinando **MVC/MVVM** para separar estrictamente las responsabilidades de la aplicación:
- **Modelo (Data Layer):** Implementado en `src/data/` (SQLite DAO y API Client). No conoce ningún detalle sobre la capa gráfica.
- **Vista (Presentation Layer):** Implementada en `src/gui/` (Prototipo Tkinter y aplicación principal en PySide6). Encargada únicamente del renderizado y captura de eventos.
- **Controlador / View-Model (Core Layer):** Ubicado en `src/core/` y `src/utils/`. Gestiona la lógica de negocio, bus de eventos mediante señales (`signals.py`) y ejecución concurrente (`threads.py`).

---

### 2. Mockups de Baja Fidelidad y Distribución de Widgets (Wireframe ASCII)

#### Vista Principal (Layout Horizontal: Sidebar + Main Area)
```text
+-----------------------------------------------------------------------+
|  NexusTech Solutions - Sistema de Gestión Client                     |
+---------------+-------------------------------------------------------+
|  [Sidebar]    |  [Header: Estado de Sincronización / Conexión API]    |
|               +-------------------------------------------------------+
|  - Dashboard  |  [Tabla / TreeView de Productos de Inventario]        |
|  - Inventario |  +----+------------------+---------+------------------+
|  - Sync API   |  | ID | Producto         | Stock   | Última Sync      |
|  - Métricas   |  +----+------------------+---------+------------------+
|  - Config     |  | 01 | Servidor Rack 2U | 14      | 10/08/2026 21:00 |
|               |  | 02 | Switch 24p GbE   | 42      | 10/08/2026 21:00 |
|               |  +----+------------------+---------+------------------+
|               |  [Botón: Agregar]  [Botón: Editar]  [Botón: Eliminar] |
|               +-------------------------------------------------------+
|               |  [Módulo de Gráficos Personalizados - QPainter]       |
+---------------+-------------------------------------------------------+
| Status: En línea | Hilo Principal: Responsivo | BD Local: Conectado     |
+-----------------------------------------------------------------------+
```
### 3. Justificación UX y Principios de Navegación
* Layout Adaptativo: Uso de contenedores dinámicos (QGridLayout y QHBoxLayout en Qt; pack/grid en Tkinter) para garantizar que la interfaz sea totalmente escalable al redimensionar la ventana.

* Principio de Responsividad: Ninguna llamada de red ni operación de escritura pesada en base de datos se ejecuta sobre el hilo principal (GUI Thread), evitando cuelgues o congelamientos ("Not Responding").

* Retroalimentación Visual: Indicadores de estado de red y barras de progreso en segundo plano alimentadas por un sistema de señales desacoplado.

### 4: Auto-crítica y Justificación de Decisiones (Rúbrica M6)
1. Arquitectura y Escalabilidad
* Elección del Framework: Se seleccionó PySide6 (Qt) como framework principal debido a su arquitectura nativa basada en el paradigma de Señales y Slots, lo que permite un desacoplamiento estricto entre la interfaz gráfica y la lógica de negocio.

* Impacto en Rendimiento y Mantenibilidad: A diferencia de frameworks más simples como Tkinter, PySide6 ofrece aceleración por hardware para gráficos personalizados (QPainter), hojas de estilo asíncronas (QSS) y un sistema multihilo nativo (QThread). Esto garantiza mantenibilidad a largo plazo y una experiencia de usuario (UX) fluida bajo el tema oscuro Catppuccin.

2. Gestión de Concurrencia y Resiliencia
* Escenario de Operación Bloqueante: Al realizar peticiones HTTP a la API REST o ejecutar transacciones intensivas en SQLite, procesar estas tareas en el hilo principal congelaría la UI.

* Solución Multihilo (QThread): Se desarrolló la clase SyncWorkerThread (src/utils/threads.py). Toda llamada I/O corre en segundo plano.

* Comunicación Segura entre Hilos: Se implementó el bus de eventos EventBus (src/core/signals.py) derivado de QObject. Las señales sync_started, progress_updated, sync_completed y sync_failed garantizan la actualización segura del thread secundario hacia la UI sin provocar condiciones de carrera (Race Conditions).

* Mecanismo de Caché y Resiliencia: En caso de fallos de red (URLError, timeouts), el cliente recupera los productos previamente guardados en la tabla api_cache de SQLite, permitiendo la continuidad operativa offline.

3. Despliegue, Portabilidad y Web (PyScript)
* Desafíos con PyInstaller: El mayor reto técnico consistió en vincular recursos estáticos (estilos .qss, DB) e importaciones ocultas de los submódulos de src/. Se resolvió configurando el archivo NexusTech.spec, mapeando las rutas en added_files e inyectando las dependencias en hiddenimports.

* Portabilidad y Migración a PyScript: Para el Módulo 6.8 se adaptó la lógica asíncrona a PyScript / Pyodide (WebAssembly). A través de pyodide.ffi.create_proxy y la API Fetch de JavaScript, la aplicación ejecuta Python dentro del navegador y manipula el DOM sin requerir un backend activo.
