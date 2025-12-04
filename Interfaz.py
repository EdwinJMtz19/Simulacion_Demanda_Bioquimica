# interface.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ProcesoDatos import cargar_limpiar_datos
from AnalisisRegresion import calcular_BOD5, stepwise_regression, calculate_correlation_matrix, stepwise_regression_od
from Visualizacion import (grafico_od_ph, grafico_temp, graficar_bod5_vs_pred_medidos, plot_bod5_comparison, grafico_temp_od_ph, 
                           plot_dqo, plot_sst, plot_dbo5, plot_residuals, graficar_prediccion_od, graficar_prediccion_dqo, plot_tss_bod5_relationship)
import io
import sys

# Paleta de colores
COLOR_DARK_TEAL = "#2B5F5F"
COLOR_TEAL = "#3D7373"
COLOR_GREEN = "#4F9F4F"
COLOR_LIGHT_GREEN = "#8BC34A"
COLOR_YELLOW_GREEN = "#C6E048"
COLOR_WHITE = "#FFFFFF"
COLOR_LIGHT_GRAY = "#F5F5F5"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Regresión para DBO5")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLOR_LIGHT_GRAY)
        
        # Variable para almacenar el archivo cargado
        self.file_path = None
        self.data = None
        self.sidebar_visible = False
        
        # Crear la pantalla inicial
        self.create_initial_screen()

    def create_initial_screen(self):
        """Crea la pantalla inicial con el botón para cargar archivo"""
        # Frame principal
        self.initial_frame = tk.Frame(self.root, bg=COLOR_LIGHT_GRAY)
        self.initial_frame.pack(fill="both", expand=True)
        
        # Contenedor central
        center_container = tk.Frame(self.initial_frame, bg=COLOR_LIGHT_GRAY)
        center_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title_label = tk.Label(
            center_container,
            text="Análisis de Regresión\npara DBO5",
            font=("Helvetica", 32, "bold"),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(pady=(0, 20))
        
        # Subtítulo
        subtitle_label = tk.Label(
            center_container,
            text="Sistema de análisis de datos del Río Atoyac",
            font=("Helvetica", 14),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_TEAL
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Botón de cargar archivo
        load_button = tk.Button(
            center_container,
            text="📁 Cargar Archivo Excel",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_GREEN,
            fg=COLOR_WHITE,
            activebackground=COLOR_LIGHT_GREEN,
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=40,
            pady=20,
            cursor="hand2",
            command=self.load_file
        )
        load_button.pack()
        
        # Hover effect
        load_button.bind("<Enter>", lambda e: load_button.config(bg=COLOR_LIGHT_GREEN))
        load_button.bind("<Leave>", lambda e: load_button.config(bg=COLOR_GREEN))

    def create_main_interface(self):
        """Crea la interfaz principal con barra lateral y área de resultados"""
        # Destruir la pantalla inicial
        self.initial_frame.destroy()
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=COLOR_LIGHT_GRAY)
        self.main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg=COLOR_DARK_TEAL, height=70)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Análisis de Regresión DBO5",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_DARK_TEAL,
            fg=COLOR_WHITE
        )
        header_label.pack(side="left", padx=30, pady=15)
        
        # Botón para recargar archivo
        reload_button = tk.Button(
            header_frame,
            text="🔄 Cambiar Archivo",
            font=("Helvetica", 11),
            bg=COLOR_TEAL,
            fg=COLOR_WHITE,
            activebackground=COLOR_GREEN,
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.reload_file
        )
        reload_button.pack(side="right", padx=30, pady=15)
        
        # Contenedor para sidebar y área de contenido
        self.content_container = tk.Frame(self.main_frame, bg=COLOR_LIGHT_GRAY)
        self.content_container.pack(fill="both", expand=True)
        
        # Área de resultados con scroll
        self.results_frame = tk.Frame(self.content_container, bg=COLOR_WHITE)
        self.results_frame.pack(side="right", fill="both", expand=True)
        
        # Canvas y scrollbar para resultados
        self.canvas = tk.Canvas(self.results_frame, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_results = tk.Frame(self.canvas, bg=COLOR_WHITE)
        
        self.scrollable_results.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_results, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mensaje inicial
        welcome_label = tk.Label(
            self.scrollable_results,
            text="👈 Menú Lateral",
            font=("Helvetica", 16),
            bg=COLOR_WHITE,
            fg=COLOR_TEAL,
            pady=100
        )
        welcome_label.pack(expand=True)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Crear sidebar oculta inicialmente
        self.create_sidebar()
        
        # Zona de activación para mostrar sidebar (borde izquierdo)
        self.activation_zone = tk.Frame(self.content_container, bg=COLOR_DARK_TEAL, width=5)
        self.activation_zone.pack(side="left", fill="y")
        self.activation_zone.bind("<Enter>", self.show_sidebar)

    def create_sidebar(self):
        """Crea la barra lateral con todos los botones"""
        self.sidebar = tk.Frame(self.content_container, bg=COLOR_DARK_TEAL, width=300)
        
        # Canvas con scroll para la sidebar
        sidebar_canvas = tk.Canvas(self.sidebar, bg=COLOR_DARK_TEAL, highlightthickness=0, width=300)
        sidebar_scrollbar = tk.Scrollbar(self.sidebar, orient="vertical", command=sidebar_canvas.yview)
        sidebar_content = tk.Frame(sidebar_canvas, bg=COLOR_DARK_TEAL)
        
        sidebar_content.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=sidebar_content, anchor="nw")
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Título de la sidebar
        sidebar_title = tk.Label(
            sidebar_content,
            text="MENÚ DE ANÁLISIS",
            font=("Helvetica", 14, "bold"),
            bg=COLOR_DARK_TEAL,
            fg=COLOR_WHITE,
            pady=20
        )
        sidebar_title.pack(fill="x")
        
        # Definir botones
        button_groups = [
            {
                "title": "Análisis Estadístico",
                "buttons": [
                    ("📊 Matriz de Correlación", self.show_correlation),
                    ("🔢 Regresión Paso a Paso", self.run_regression)
                ]
            },
            {
                "title": "Visualización",
                "buttons": [
                    ("🌡️ Temperatura y OD/pH", self.vista_temp_od_ph),
                    ("🌡️ Temperatura", self.vista_temp),
                    ("💧 OD y pH", self.vista_od_th),
                    ("🔬 DQO", self.vista_dqo),
                    ("🧪 DBO5", self.vista_dbo5),
                    ("⚗️ SST", self.vista_sst)
                ]
            },
            {
                "title": "Predicción",
                "buttons": [
                    ("📈 Comparación DBO5", self.vista_dbo5_mes_vs_pred),
                    ("📉 DBO5 vs Predicción", self.vista_dbo5_vs_pred),
                    ("⚠️ Errores", self.vista_residuals),
                    ("🎯 Predicción OD", self.vista_tss_bod5),
                    ("🎯 Predicción DQO", self.run_regression_dqo)
                ]
            }
        ]
        
        # Crear grupos de botones
        for group in button_groups:
            # Título del grupo
            group_label = tk.Label(
                sidebar_content,
                text=group["title"],
                font=("Helvetica", 11, "bold"),
                bg=COLOR_DARK_TEAL,
                fg=COLOR_YELLOW_GREEN,
                anchor="w",
                padx=20,
                pady=5
            )
            group_label.pack(fill="x", pady=(15, 5))
            
            # Botones del grupo
            for btn_text, btn_command in group["buttons"]:
                button = tk.Button(
                    sidebar_content,
                    text=btn_text,
                    font=("Helvetica", 10),
                    bg=COLOR_TEAL,
                    fg=COLOR_WHITE,
                    activebackground=COLOR_LIGHT_GREEN,
                    activeforeground=COLOR_WHITE,
                    relief="flat",
                    padx=15,
                    pady=10,
                    cursor="hand2",
                    anchor="w",
                    command=btn_command
                )
                button.pack(fill="x", padx=10, pady=2)
                
                # Hover effects
                def on_enter(e, btn=button):
                    btn.config(bg=COLOR_LIGHT_GREEN)
                
                def on_leave(e, btn=button):
                    btn.config(bg=COLOR_TEAL)
                
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)
        
        # Botón para ocultar sidebar
        hide_button = tk.Button(
            sidebar_content,
            text="◀ Ocultar",
            font=("Helvetica", 10, "bold"),
            bg=COLOR_GREEN,
            fg=COLOR_WHITE,
            activebackground=COLOR_DARK_TEAL,
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.hide_sidebar
        )
        hide_button.pack(fill="x", padx=10, pady=20)
        
        # Bind para ocultar al salir
        self.sidebar.bind("<Leave>", lambda e: self.check_hide_sidebar(e))

    def show_sidebar(self, event=None):
        """Muestra la barra lateral"""
        if not self.sidebar_visible:
            self.sidebar.pack(side="left", fill="y", before=self.results_frame)
            self.sidebar_visible = True

    def hide_sidebar(self, event=None):
        """Oculta la barra lateral"""
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False

    def check_hide_sidebar(self, event):
        """Verifica si el mouse salió completamente de la sidebar"""
        # Esperar un momento antes de ocultar
        self.root.after(500, lambda: self.hide_sidebar_delayed(event))

    def hide_sidebar_delayed(self, event):
        """Oculta la sidebar con retraso"""
        # Verificar si el mouse está fuera de la sidebar
        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        sidebar_x = self.sidebar.winfo_rootx()
        sidebar_y = self.sidebar.winfo_rooty()
        sidebar_width = self.sidebar.winfo_width()
        sidebar_height = self.sidebar.winfo_height()
        
        if not (sidebar_x <= x <= sidebar_x + sidebar_width and 
                sidebar_y <= y <= sidebar_y + sidebar_height):
            self.hide_sidebar()

    def add_result_section(self, title, content):
        """Agrega una nueva sección de resultados"""
        # Frame para la sección
        section_frame = tk.Frame(self.scrollable_results, bg=COLOR_WHITE, relief="solid", borderwidth=1)
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Header de la sección
        header = tk.Frame(section_frame, bg=COLOR_DARK_TEAL)
        header.pack(fill="x")
        
        title_label = tk.Label(
            header,
            text=title,
            font=("Helvetica", 14, "bold"),
            bg=COLOR_DARK_TEAL,
            fg=COLOR_WHITE,
            anchor="w",
            padx=15,
            pady=10
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Botón para cerrar la sección
        close_button = tk.Button(
            header,
            text="✕",
            font=("Helvetica", 12, "bold"),
            bg=COLOR_DARK_TEAL,
            fg=COLOR_WHITE,
            activebackground=COLOR_TEAL,
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=10,
            cursor="hand2",
            command=lambda: section_frame.destroy()
        )
        close_button.pack(side="right")
        
        # Contenido de la sección
        content_frame = tk.Frame(section_frame, bg=COLOR_WHITE)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Text widget con scroll
        text_scroll = tk.Scrollbar(content_frame)
        text_scroll.pack(side="right", fill="y")
        
        text_widget = tk.Text(
            content_frame,
            wrap="word",
            font=("Courier", 9),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_DARK_TEAL,
            relief="flat",
            padx=10,
            pady=10,
            yscrollcommand=text_scroll.set
        )
        text_widget.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=text_widget.yview)
        
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        # Scroll to the new section
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def load_file(self):
        """Dialogo para cargar archivo"""
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de Excel",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if not file_path:
            return

        self.file_path = file_path
        try:
            # Cargar y limpiar los datos
            self.data = cargar_limpiar_datos(self.file_path)
            messagebox.showinfo("✅ Éxito", "Datos cargados y limpiados exitosamente.")
            # Crear la interfaz principal
            self.create_main_interface()
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo cargar el archivo:\n{e}")

    def reload_file(self):
        """Recargar archivo y volver a la pantalla inicial"""
        self.data = None
        self.file_path = None
        # Destruir todo y recrear pantalla inicial
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_initial_screen()

    def show_correlation(self):
        """Muestra la matriz de correlación en el área de resultados"""
        if self.data is not None:
            # Capturar la salida
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            correlation_matrix = calculate_correlation_matrix(self.data, target_column='DBO5')
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            # Agregar resultado
            self.add_result_section("📊 Matriz de Correlación", output)
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            
    def run_regression(self):
        """Ejecuta la regresión y muestra resultados en el área"""
        if self.data is not None:
            # Capturar la salida
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            X = self.data[['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA']]
            y = self.data['DBO5']
            self.model = stepwise_regression(X, y)
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            # Agregar resultado
            self.add_result_section("🔢 Regresión Paso a Paso", output)
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")

    def vista_temp_od_ph(self):
        observaciones = range(len(self.data))
        grafico_temp_od_ph(observaciones, self.data['TEMP_AGUA'], self.data['OD_mg/L'], self.data['pH_CAMPO'])

    def vista_temp(self):
        observaciones = range(len(self.data))
        grafico_temp(observaciones, self.data['TEMP_AGUA'])
    
    def vista_od_th(self):
        observaciones = range(len(self.data))
        grafico_od_ph(observaciones, self.data['OD_mg/L'], self.data['pH_CAMPO'])
    
    def vista_dqo(self):
        observaciones = range(len(self.data))
        plot_dqo(observaciones, self.data['DQO_TOT'])

    def vista_sst(self):
        observaciones = range(len(self.data))
        plot_sst(observaciones, self.data['SST'])

    def vista_dbo5(self):
        observaciones = range(len(self.data))
        plot_dbo5(observaciones, self.data['DBO5'])

    def vista_dbo5_vs_pred(self):
        observaciones = range(len(self.data))
        OD_values = self.data['OD_mg/L']
        DQO_values = self.data['DQO_TOT']
        BOD5_values = self.data['DBO5']
        BOD5_predichos = calcular_BOD5(OD_values, DQO_values)
        graficar_bod5_vs_pred_medidos(BOD5_values, BOD5_predichos)

    def vista_dbo5_mes_vs_pred(self):
        observaciones = range(len(self.data))
        OD_values = self.data['OD_mg/L']
        DQO_values = self.data['DQO_TOT']
        BOD5_values = self.data['DBO5']
        BOD5_predichos = calcular_BOD5(OD_values, DQO_values)
        plot_bod5_comparison(observaciones, BOD5_values, BOD5_predichos)

    def vista_residuals(self):
        if hasattr(self, 'model'):
            y_pred = self.model.predict()
            plot_residuals(self.data['DBO5'], y_pred)
        else:
            messagebox.showerror("Error", "Por favor, ejecute la regresión primero.")
    
    def vista_tss_bod5(self):
        if self.data is not None:
            tss_values = self.data['DQO_TOT']
            bod5_values = self.data['DBO5']
            sorted_data = self.data.sort_values(by='DQO_TOT', ascending=False)
            cod_sorted = sorted_data['DQO_TOT']
            dbodbo5_measured_sorted = sorted_data['DBO5']
            plot_tss_bod5_relationship(cod_sorted, dbodbo5_measured_sorted)
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
    
    def run_regression_dqo(self):
        if self.data is not None:
            X = self.data['DQO_TOT']
            y = self.data['DBO5']
            plot_tss_bod5_relationship(X, y)
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")