# Registro de Decisiones Técnicas y Auto-crítica - Módulo 6
**Proyecto:** NexusTech Solutions · Sistema de Gestión Integral Multiplataforma  
**Programa:** Certificación Python SSR - Módulo 6  
**Desarrollador:** Nayib de la Cruz Márquez  

---

## Auto-crítica y Respuestas Reflexivas

### 1. Arquitectura y Escalabilidad
Se eligió **PySide6 (Qt para Python)** como framework principal debido a su arquitectura avanzada **Modelo-Vista (MVVM/MVC)**, su robusto bus de **Señales y Slots** para desacoplar componentes y la capacidad de personalizar widgets nativos usando `QPainter` y hojas de estilo QSS. Aunque Tkinter se utilizó para el prototipo inicial por su ligereza, PySide6 ofrece un rendimiento superior en renderizado, mayor mantenibilidad en proyectos de escala corporativa y una experiencia de usuario (UX) moderna y adaptativa.

### 2. Gestión de Concurrencia y Resiliencia
Las peticiones HTTP a APIs remotas o consultas pesadas en SQLite representan operaciones bloqueantes que congelarían la GUI si corrieran en el hilo principal. Se resolvió implementando **`QThread` y trabajadores asíncronos (`ApiWorker`)**. La comunicación segura entre hilos se garantiza exclusivamente mediante señales Qt (`Signal`), transmitiendo diccionarios de datos e indicadores de progreso hacia el hilo principal de la UI sin riesgo de *race conditions*. Si la API externa falla, el sistema conmuta automáticamente a la base de datos local SQLite (`api_cache`), garantizando disponibilidad 100% offline.

### 3. Despliegue y Portabilidad
El mayor desafío en PyInstaller fue la resolución de dependencias implícitas de PySide6 y la inclusión de recursos estáticos (`_MEIPASS`). Se solucionó configurando explícitamente el archivo `.spec` para empaquetar carpetas de datos y hooks de importación. Para garantizar la migración futura hacia entornos web, la lógica de negocio y de consumo de API se mantuvo totalmente independiente de la UI, permitiendo que **PyScript (WASM)** consuma exactamente la misma estructura de datos directamente desde el navegador.