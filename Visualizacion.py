# Visualizacion.py
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from AnalisisRegresion import calcular_BOD5_OD, stepwise_regression_dqo, stepwise_regression_od

def grafico_temp_od_ph(observaciones, temperatura, od, ph):
    plt.figure(figsize=(14, 8))

    # Gráfico de temperatura
    plt.subplot(1, 2, 1)
    plt.plot(observaciones, temperatura, 'o-', color="dodgerblue")
    plt.xlabel("Observaciones")
    plt.ylabel("Temperatura (°C)")
    plt.title("Variaciones de temperatura del Río Atoyac ")
    plt.ylim(0, 30)
    plt.yticks(range(0, 31, 5))

    # Gráfico de OD y pH
    plt.subplot(1, 2, 2)
    plt.plot(observaciones, od, 'o-', label="OD (mg/L)", color="dodgerblue")
    plt.plot(observaciones, ph, 'o-', label="pH", color="gray")
    plt.xlabel("Observaciones")
    plt.ylabel("Valor del parámetro")
    plt.title("Valores de OD y pH en las muestras")
    plt.legend()
    plt.ylim(-1, 10)
    plt.yticks(range(-1, 10, 1))

    plt.tight_layout()
    plt.show()
def grafico_od_ph(observaciones, od, ph):
    plt.figure(figsize=(14, 8))

    # Gráfico de OD y pH
    plt.plot(observaciones, od, 'o-', label="OD (mg/L)", color="dodgerblue")
    plt.plot(observaciones, ph, 'o-', label="pH", color="gray")
    plt.xlabel("Observaciones")
    plt.ylabel("Valor del parámetro")
    plt.title("Valores de OD y pH del Río Atoyac, Puebla")
    plt.legend()
    plt.ylim(-1, 10)
    plt.yticks(range(-1, 10, 1))
    plt.tight_layout()
    plt.show()
def grafico_temp(observaciones, temperatura):
    plt.figure(figsize=(14, 8))
    # Gráfico de temperatura
    plt.plot(observaciones, temperatura, 'o-', color="dodgerblue")
    plt.xlabel("Observaciones")
    plt.ylabel("Temperatura (°C)")
    plt.title("Variaciones de temperatura del Río Atoyac, Puebla")
    plt.ylim(0, 30)
    plt.yticks(range(0, 31, 5))

    plt.tight_layout()
    plt.show()
    #GRAFICA SST
def plot_sst(observaciones, sst):
    plt.figure(figsize=(10, 6))
    plt.plot(observaciones, sst, 'o-', color='orange', label='TSS (mg/L)', markersize=5)
    plt.xlabel("Observaciones")
    plt.ylabel("Valor Parametro")
    plt.yscale("log")
    plt.title("SSt 8 años")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

    #GRAFICA DQO
def plot_dqo(observaciones, dqo):
    plt.figure(figsize=(10, 6))
    plt.plot(observaciones, dqo, 'd-', color='gray', label='DQO (mg/L)', markersize=5)
    plt.xlabel("Observaciones")
    plt.ylabel("Valor Parametro")
    plt.yscale("log")
    plt.title("COD 8 años")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

    #GRAFICA DBO5
def plot_dbo5(observaciones, dbo5):
    plt.figure(figsize=(10, 6))
    plt.plot(observaciones, dbo5, 'o-', color='green', label='BOD5 (mg/L)', markersize=5)
    plt.xlabel("Observaciones")
    plt.ylabel("Valor Parametro")
    plt.yscale("log")
    plt.title("BOD5 8 años")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()
def plot_dqo_sst_dbo5(observaciones, dqo, sst, dbo5):
    plt.figure(figsize=(10, 6))
    plt.yscale('log')

    plt.plot(observaciones, dqo, 'd-', color='gray', label='COD (mg/L)', markersize=5)
    plt.plot(observaciones, sst, 'o-', color='orange', label='TSS (mg/L)', markersize=5)
    plt.plot(observaciones, dbo5, 'o-', color='yellow', label='BOD5 (mg/L)', markersize=5)

    plt.xlabel('Observaciones')
    plt.ylabel('Valor Parametro')
    plt.title('SST, COD, BOD5 8 años')
    plt.legend()
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.show()
def plot_dbo5_vs_predicted(dbo5, y_pred):
    plt.figure(figsize=(8, 6))
    plt.scatter(dbo5, y_pred, color="purple", alpha=0.7, label="Valores Predichos")
    plt.plot([dbo5.min(), dbo5.max()], [dbo5.min(), dbo5.max()], 'k--', lw=2)
    plt.xlabel("DBO5 Medida")
    plt.ylabel("DBO5 Prevista")
    plt.title("DBO5 medida vs. valores predichos")
    print("Rango de DBO5 Medida:", dbo5.min(), "-", dbo5.max())
    print("Rango de DBO5 Predicha:", y_pred.min(), "-", y_pred.max())
    plt.show()
def plot_residuals(dbo5, y_pred):
    residuos = dbo5 - y_pred

    plt.figure(figsize=(14, 8))

    # Diferencia entre DBO5 medida y DBO5 predicha
    plt.subplot(1, 2, 1)
    plt.scatter(dbo5, dbo5 - y_pred, color="red", alpha=0.7)
    plt.axhline(0, color='black', linestyle='--')
    plt.xlabel("DBO5 Medida")
    plt.ylabel("Diferencia (DBO5 Medida - DBO5 Predicha)")
    plt.title("Diferencia entre DBO5 Medida y DBO5 Predicha")

    # Gráfico de residuos vs. valores predichos
    plt.subplot(1, 2, 2)
    plt.scatter(y_pred, residuos, color="green", alpha=0.7)
    plt.axhline(0, color='black', linestyle='--')
    plt.xlabel("DBO5 Prevista")
    plt.ylabel("Residuos")
    plt.title("Gráfico de residuos vs. DBO5 predicha")

    plt.tight_layout()
    plt.show()

    # Función para crear el gráfico de dispersión
def graficar_bod5_vs_pred_medidos(BOD5_medidos, BOD5_predichos):
    
    # Crear gráfico de dispersión
    plt.figure(figsize=(8, 6))
    plt.scatter(BOD5_medidos, BOD5_predichos, color='blue', label='Valores Medidos vs Predichos')

    # Línea de identidad (donde los valores medidos son iguales a los predichos)
    plt.plot([min(BOD5_medidos), max(BOD5_medidos)], [min(BOD5_medidos), max(BOD5_medidos)], 'r--', label='Línea de Identidad')

    # Etiquetas y título
    plt.title('Fitness of Measured BOD5 vs Predicted BOD5 for 333 Observations')
    plt.xlabel('Measured BOD5')
    plt.ylabel('Predicted BOD5')
    
    # Mostrar la leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.show()
def plot_bod5_comparison(observations, measured, predicted):
    """
    Función para graficar los valores medidos y predichos de DBO5 en función de las observaciones.
    
    Parámetros:
    observations (array-like): Lista o array con las observaciones (índices o fechas).
    measured (array-like): Lista o array con los valores medidos de DBO5.
    predicted (array-like): Lista o array con los valores predichos de DBO5.
    
    Devuelve:
    None (muestra los gráficos de líneas)
    """
    plt.figure(figsize=(10, 6))

    # Graficar los valores medidos
    plt.plot(observations, measured, color='blue', label='Valores Medidos', marker='o', linestyle='-', markersize=5)

    # Graficar los valores predichos
    plt.plot(observations, predicted, color='red', label='Valores Predichos', marker='o', linestyle='-', markersize=5)

    # Añadir título y etiquetas
    plt.title('Comparación de Valores Medidos y Predichos de DBO5')
    plt.xlabel('Observaciones')
    plt.ylabel('DBO5')
    
    # Añadir leyenda
    plt.legend()

    # Mostrar la gráfica
    plt.grid(True)
    plt.show()
def graficar_prediccion_dqo(COD, BOD5_observado):
    # Crear el modelo de regresión lineal
    model = LinearRegression()
    
    # Ajustar el modelo a los datos
    model.fit(COD.reshape(-1, 1), BOD5_observado)
    
    # Hacer las predicciones usando el modelo ajustado
    BOD5_predicho = model.predict(COD.reshape(-1, 1))
    
    # Generar un rango de valores para la línea de predicción
    COD_range = np.linspace(min(COD), max(COD), 500).reshape(-1, 1)
    BOD5_line = model.predict(COD_range)
    
    # Crear la gráfica
    plt.figure(figsize=(8, 5))
    plt.scatter(COD, BOD5_observado, color='blue', label='BOD5 Observado', alpha=0.7)
    plt.scatter(COD, BOD5_predicho, color='orange', label='BOD5 Predicho', alpha=0.7)
    plt.plot(COD_range, BOD5_line, color='black', label='Línea de Predicción (Regresión)', linewidth=2)
    
    # Personalización de la gráfica
    plt.title('DQO vs BOD5 - Predicción Lineal', fontsize=14)
    plt.xlabel('DQO', fontsize=12)
    plt.ylabel('BOD5', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()
def graficar_prediccion_od(OD, BOD5_observado):
    # Crear el modelo de regresión lineal
    model = LinearRegression()
    
    # Ajustar el modelo a los datos
    model.fit(OD.reshape(-1, 1), BOD5_observado)
    
    # Hacer las predicciones usando el modelo ajustado
    BOD5_predicho = model.predict(OD.reshape(-1, 1))
    
    # Generar un rango de valores para la línea de predicción
    OD_range = np.linspace(min(OD), max(OD), 500).reshape(-1, 1)
    BOD5_line = model.predict(OD_range)
    
    # Crear la gráfica
    plt.figure(figsize=(8, 5))
    plt.scatter(OD, BOD5_observado, color='blue', label='BOD5 Observado', alpha=0.7)
    plt.scatter(OD, BOD5_predicho, color='orange', label='BOD5 Predicho', alpha=0.7)
    plt.plot(OD_range, BOD5_line, color='black', label='Línea de Predicción (Regresión)', linewidth=2)
    
    # Personalización de la gráfica
    plt.title('SST vs BOD5 - Predicción Lineal', fontsize=14)
    plt.xlabel('SST', fontsize=12)
    plt.ylabel('BOD5', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()
def plot_tss_bod5_relationship(cod, dbo5):
    model = stepwise_regression_od(cod, dbo5)
    BOD5_predichos = calcular_BOD5_OD(cod)
    plt.figure(figsize=(10, 6))

    # Graficar los valores medidos
    plt.plot(cod, BOD5_predichos, color='blue', label='Valores Medidos', marker='o', linestyle='-', markersize=5)

    # Graficar los valores predichos
    plt.plot(cod, BOD5_predichos, color='red', label='Valores Predichos', marker='o', linestyle='-', markersize=5)

    # Añadir título y etiquetas
    plt.title('Comparación de Valores Medidos y Predichos de DBO5')
    plt.xlabel('Observaciones')
    plt.ylabel('DBO5')
    
    # Añadir leyenda
    plt.legend()

    # Mostrar la gráfica
    plt.grid(True)
    plt.show()
    

