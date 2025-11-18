# ProcesoDatos.py
import pandas as pd
import numpy as np

def cargar_limpiar_datos(file_path):
    # Cargar y limpiar datos
    data = pd.read_excel(file_path)
    data_cleaned = data.copy()
    data_cleaned = data_cleaned.replace('<1', np.nan).replace('<10', np.nan)
    data_cleaned = data_cleaned.apply(pd.to_numeric, errors='coerce')
    
    # Quitar filas con valores nulos en columnas relevantes
    data_cleaned = data_cleaned.dropna(subset=['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA', 'DBO5'])
    return data_cleaned

def load_validation_data(file_path):
    # Cargar datos de validación (solo 2012 y 2013)
    data = pd.read_excel(file_path)
    validation_data = data[(data['AÑO'] == 2012) | (data['AÑO'] == 2013)]
    validation_data = validation_data.dropna(subset=['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA', 'DBO5'])
    
    return validation_data
