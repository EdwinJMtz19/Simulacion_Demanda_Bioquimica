# interface.py
import tkinter as tk
from tkinter import filedialog, messagebox
from ProcesoDatos import cargar_limpiar_datos
from AnalisisRegresion import calcular_BOD5, stepwise_regression, calculate_correlation_matrix, stepwise_regression_od
from Visualizacion import (grafico_od_ph, grafico_temp, graficar_bod5_vs_pred_medidos, plot_bod5_comparison, grafico_temp_od_ph, 
                           plot_dqo, plot_sst, plot_dbo5, plot_residuals, graficar_prediccion_od, graficar_prediccion_dqo, plot_tss_bod5_relationship)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Regresión para DBO5")
        
        # Variable para almacenar el archivo cargado
        self.file_path = None
        self.data = None
         # Cargar archivo
        self.load_file()
        # Crear botones e interfaz
        self.create_widgets()

    def create_widgets(self):
        # Botón para mostrar matriz de correlación
        self.correlation_button = tk.Button(self.root, text="Mostrar Matriz de Correlación", command=self.show_correlation)
        self.correlation_button.pack(pady=10)
        
        # Botón para realizar la regresión paso a paso
        self.regression_button = tk.Button(self.root, text="Ejecutar Regresión Paso a Paso", command=self.run_regression)
        self.regression_button.pack(pady=10)
        
        # Botones para visualizar gráficos
        self.plot_buttons = [
            tk.Button(self.root, text="Gráfico de Temperatura y OD/pH", command=self.vista_temp_od_ph),
            tk.Button(self.root, text="Gráfico de Temperatura ", command=self.vista_temp),
            tk.Button(self.root, text="Gráfico de OD y PH ", command=self.vista_od_th),
            tk.Button(self.root, text="Gráfico de DQO", command=self.vista_dqo),
            tk.Button(self.root, text="Gráfico de DBO", command=self.vista_dbo5),
            tk.Button(self.root, text="Gráfico de SST", command=self.vista_sst),
            tk.Button(self.root, text="Gráfico de Comparacion DBO5 vs. Predicción", command=self.vista_dbo5_mes_vs_pred),
            tk.Button(self.root, text="Gráfico de DBO5 vs. Predicción", command=self.vista_dbo5_vs_pred),
            tk.Button(self.root, text="Gráfico de Errores", command=self.vista_residuals),
            tk.Button(self.root, text="Gráfico de prediccion de OD", command=self.vista_tss_bod5),
            tk.Button(self.root, text="Gráfico de prediccion de DQO", command=self.run_regression_dqo)
        ]

        
        for button in self.plot_buttons:
            button.pack(pady=5)

    def load_file(self):
        # Dialogo para cargar archivo
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de Excel",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if not file_path:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
            self.root.quit()
            return

        self.file_path = file_path
        try:
            # Cargar y limpiar los datos
            self.data = cargar_limpiar_datos(self.file_path)
            messagebox.showinfo("Éxito", "Datos cargados y limpiados exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
            self.root.quit()
            

    def show_correlation(self):
        if self.data is not None:
            correlation_matrix = calculate_correlation_matrix(self.data, target_column='DBO5')
            messagebox.showinfo("Matriz de Correlación", correlation_matrix.to_string())
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            
    def run_regression(self):
        if self.data is not None:
            X = self.data[['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA']]
            y = self.data['DBO5']
            self.model = stepwise_regression(X, y)
            messagebox.showinfo("Regresión", "Regresión paso a paso completada.")
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
            # Extraer los valores de las columnas
            OD_values = self.data['OD_mg/L']  # Asumiendo que 'DQ' es TSS
            DQO_values = self.data['DQO_TOT']  # Asumiendo que 'DQO_TOT' es OD_mg/L
            BOD5_values = self.data['DBO5']  # Asumiendo que 'DBO5' son los valores de BOD5
            BOD5_predichos = calcular_BOD5(OD_values, DQO_values)

            # Llamar a la función para graficar
            graficar_bod5_vs_pred_medidos(BOD5_values, BOD5_predichos)

    def vista_dbo5_mes_vs_pred(self):
            observaciones = range(len(self.data))
            # Extraer los valores de las columnas
            OD_values = self.data['OD_mg/L']  # Asumiendo que 'DQ' es TSS
            DQO_values = self.data['DQO_TOT']  # Asumiendo que 'DQO_TOT' es OD_mg/L
            BOD5_values = self.data['DBO5']  # Asumiendo que 'DBO5' son los valores de BOD5
            BOD5_predichos = calcular_BOD5(OD_values, DQO_values)

            # Llamar a la función para graficar
            plot_bod5_comparison(observaciones,BOD5_values, BOD5_predichos)


    def vista_residuals(self):
        if hasattr(self, 'model'):
            y_pred = self.model.predict()
            plot_residuals(self.data['DBO5'], y_pred)
        else:
            messagebox.showerror("Error", "Por favor, ejecute la regresión primero.")
    
    def run_regression(self):
        if self.data is not None:
            X = self.data[['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA']]
            y = self.data['DBO5']
            self.model = stepwise_regression(X, y)
            messagebox.showinfo("Regresión", "Regresión paso a paso completada.")
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
    def vista_dqo_dbo5_vs_pred(self):
        # Extraer los valores de las columnas
        DQO_values = self.data['DQO_TOT'].values  # Asumiendo que 'DQO_TOT' es OD_mg/L
        BOD5_values = self.data['DBO5'].values  # Asumiendo que 'DBO5' son los valores de BOD5
        #BOD5_predichos = calcular_BOD5(DQO_values, BOD5_values)

        # Llamar a la función para graficar
        graficar_prediccion_dqo(DQO_values,BOD5_values)

    def vista_od_dbo5_vs_pred(self):
        # Extraer los valores de las columnas
        OD_values = self.data['OD_mg/L'].values  # Convertir a array de NumPy
        BOD5_values = self.data['DBO5'].values  # Convertir a array de NumPy
        # Llamar a la función para graficar
        graficar_prediccion_od(OD_values, BOD5_values)
    
    def vista_tss_bod5(self):
        if self.data is not None:
            tss_values = self.data['DQO_TOT']  # Columna de TSS (Sólidos Suspendidos Totales)
            bod5_values = self.data['DBO5']  # Columna de BOD5 (Demanda Biológica de Oxígeno)
            sorted_data = self.data.sort_values(by='DQO_TOT', ascending=False)

            # Obtener los valores ordenados
            cod_sorted = sorted_data['DQO_TOT']
            dbodbo5_measured_sorted = sorted_data['DBO5']
            # Llamar a la función de graficado
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
