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