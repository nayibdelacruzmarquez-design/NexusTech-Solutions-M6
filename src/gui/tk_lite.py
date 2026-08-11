import tkinter as tk
from tkinter import messagebox, ttk


class NexusLiteApp(tk.Tk):
    """
    Prototipo funcional 'Lite' de NexusTech Solutions utilizando Tkinter.
    Demuestra navegación de vistas, eventos (bindings) y gestores de geometría (pack y grid).
    """

    def __init__(self):
        super().__init__()

        self.title("NexusTech Solutions - Prototipo Lite (Tkinter)")
        self.geometry("750x500")
        self.minsize(650, 400)

        # Estado básico de la sesión / vista
        self.current_user = "Ing. Nayib"

        # --- 1. CABECERA / HEADER (Gestor de Geometría: PACK) ---
        self.header_frame = tk.Frame(self, bg="#1E1E2E", height=50)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        self.lbl_title = tk.Label(
            self.header_frame,
            text="NexusClient · Prototipo Tkinter Lite",
            font=("Arial", 14, "bold"),
            fg="#FFFFFF",
            bg="#1E1E2E",
        )
        self.lbl_title.pack(side=tk.LEFT, padx=15, pady=10)

        self.lbl_user = tk.Label(
            self.header_frame,
            text=f"Usuario: {self.current_user}",
            font=("Arial", 10),
            fg="#A6ADC8",
            bg="#1E1E2E",
        )
        self.lbl_user.pack(side=tk.RIGHT, padx=15)

        # --- 2. BARRA DE ESTADO / FOOTER (Se crea aquí para evitar AttributeError) ---
        self.status_bar = tk.Label(
            self,
            text="Estado: Cargando interfaz...",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#11111B",
            fg="#A6ADC8",
            font=("Arial", 9),
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # --- 3. ÁREA DE NAVEGACIÓN Y CONTENIDO (Gestor de Geometría: PACK & GRID) ---
        self.main_container = tk.Frame(self, bg="#2D2D3F")
        self.main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Panel Lateral (Sidebar) para Cambio de Vistas
        self.sidebar_frame = tk.Frame(
            self.main_container, bg="#181825", width=160
        )
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.btn_view_inventory = tk.Button(
            self.sidebar_frame,
            text="📦 Inventario",
            font=("Arial", 10, "bold"),
            bg="#313244",
            fg="#CDD6F4",
            relief=tk.FLAT,
            command=self.show_inventory_view,
        )
        self.btn_view_inventory.pack(fill=tk.X, padx=10, pady=(20, 5))

        self.btn_view_register = tk.Button(
            self.sidebar_frame,
            text="➕ Nuevo Producto",
            font=("Arial", 10, "bold"),
            bg="#313244",
            fg="#CDD6F4",
            relief=tk.FLAT,
            command=self.show_register_view,
        )
        self.btn_view_register.pack(fill=tk.X, padx=10, pady=5)

        # Panel de Contenido Dinámico (Contenedor Intercambiable)
        self.content_frame = tk.Frame(self.main_container, bg="#1E1E2E")
        self.content_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        # Vistas de la Aplicación
        self.view_inventory = tk.Frame(self.content_frame, bg="#1E1E2E")
        self.view_register = tk.Frame(self.content_frame, bg="#1E1E2E")

        # Inicializar Componentes de cada vista
        self._build_inventory_view()
        self._build_register_view()

        # Mostrar la vista por defecto ahora que status_bar ya existe
        self.show_inventory_view()

    def _build_inventory_view(self):
        """Construye la vista de Inventarios utilizando GRID y Widgets de Control."""
        lbl_sub = tk.Label(
            self.view_inventory,
            text="Listado de Inventario Local (Prototipo)",
            font=("Arial", 12, "bold"),
            fg="#89B4FA",
            bg="#1E1E2E",
        )
        lbl_sub.pack(anchor=tk.W, pady=(0, 10))

        # Lista interactiva
        self.items_listbox = tk.Listbox(
            self.view_inventory,
            bg="#313244",
            fg="#CDD6F4",
            selectbackground="#89B4FA",
            selectforeground="#11111B",
            font=("Consolas", 10),
            height=12,
        )
        self.items_listbox.pack(fill=tk.BOTH, expand=True)

        # Datos Mock de inicio
        for item in [
            "ID: 01 | Servidor Rack 2U - Stock: 14",
            "ID: 02 | Switch 24-Ports - Stock: 42",
            "ID: 03 | Enrutador Gigabit - Stock: 8",
        ]:
            self.items_listbox.insert(tk.END, item)

        # BINDING DE EVENTOS: Doble clic sobre un elemento de la lista
        self.items_listbox.bind("<Double-Button-1>", self._on_item_double_click)

    def _build_register_view(self):
        """Construye la vista de Registro usando GRID para la distribución de los campos."""
        lbl_sub = tk.Label(
            self.view_register,
            text="Registro de Nuevo Material",
            font=("Arial", 12, "bold"),
            fg="#A6E3A1",
            bg="#1E1E2E",
        )
        lbl_sub.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Campos de entrada utilizando GRID
        tk.Label(
            self.view_register,
            text="Nombre del Producto:",
            fg="#CDD6F4",
            bg="#1E1E2E",
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_name = tk.Entry(
            self.view_register, width=30, bg="#313244", fg="#FFFFFF"
        )
        self.entry_name.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(
            self.view_register, text="Stock Inicial:", fg="#CDD6F4", bg="#1E1E2E"
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_stock = tk.Entry(
            self.view_register, width=15, bg="#313244", fg="#FFFFFF"
        )
        self.entry_stock.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # BINDING DE EVENTOS: Presionar Tecla ENTER en la entrada de stock
        self.entry_stock.bind("<Return>", lambda event: self._save_product())

        btn_save = tk.Button(
            self.view_register,
            text="Guardar Registro",
            bg="#A6E3A1",
            fg="#11111B",
            font=("Arial", 9, "bold"),
            command=self._save_product,
        )
        btn_save.grid(row=3, column=1, sticky="w", pady=15)

    def show_inventory_view(self):
        """Oculta otras vistas y muestra la vista de inventario."""
        self.view_register.pack_forget()
        self.view_inventory.pack(fill=tk.BOTH, expand=True)
        self.status_bar.config(
            text="Navegación: Vista de Inventario | Prototipo Lite Listo"
        )

    def show_register_view(self):
        """Oculta otras vistas y muestra el formulario de registro."""
        self.view_inventory.pack_forget()
        self.view_register.pack(fill=tk.BOTH, expand=True)
        self.status_bar.config(text="Navegación: Formulario de Registro")

    def _save_product(self):
        """Captura datos, valida y agrega al listbox (simulación de registro)."""
        name = self.entry_name.get().strip()
        stock = self.entry_stock.get().strip()

        if not name or not stock:
            messagebox.showwarning(
                "Atención", "Por favor completa todos los campos."
            )
            return

        new_entry = f"ID: NEW | {name} - Stock: {stock}"
        self.items_listbox.insert(tk.END, new_entry)

        # Limpiar entradas
        self.entry_name.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

        messagebox.showinfo(
            "Éxito", f"Producto '{name}' agregado al prototipo."
        )
        self.show_inventory_view()

    def _on_item_double_click(self, event):
        """Manejo del evento binding de doble clic en elementos."""
        selection = self.items_listbox.curselection()
        if selection:
            item_text = self.items_listbox.get(selection[0])
            messagebox.showinfo(
                "Detalle del Elemento", f"Seleccionado: {item_text}"
            )


if __name__ == "__main__":
    app = NexusLiteApp()
    app.mainloop()