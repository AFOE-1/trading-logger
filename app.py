import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import requests

# Crear un DataFrame vacío para almacenar las operaciones
columns = ['Fecha', 'Hora', 'Tipo de Opción', 'Par de Divisas', 'Monto Invertido', 'Resultado', 'Ganancia/Pérdida', 'Porcentaje de Ganancia/Pérdida']
df = pd.DataFrame(columns=columns)

# Función para registrar una nueva operación
def registrar_operacion(tipo_opcion, par_divisas, monto_invertido, resultado, ganancia_perdida):
    # Obtener la fecha y hora actual
    fecha_hora = datetime.now()
    fecha = fecha_hora.strftime('%Y-%m-%d')
    hora = fecha_hora.strftime('%H:%M:%S')
    
    # Calcular el porcentaje de ganancia/pérdida
    if monto_invertido != 0:
        porcentaje = (ganancia_perdida / monto_invertido) * 100
    else:
        porcentaje = 0
    
    # Crear un diccionario con los datos de la operación
    operacion = {
        'Fecha': fecha,
        'Hora': hora,
        'Tipo de Opción': tipo_opcion,
        'Par de Divisas': par_divisas,
        'Monto Invertido': monto_invertido,
        'Resultado': resultado,
        'Ganancia/Pérdida': ganancia_perdida,
        'Porcentaje de Ganancia/Pérdida': porcentaje
    }
    
    # Añadir la operación al DataFrame
    global df
    df = df.append(operacion, ignore_index=True)
    
    # Guardar el DataFrame en un archivo CSV
    df.to_csv('registro_operaciones.csv', index=False)
    
    st.success("Operación registrada con éxito!")

# Función para filtrar las operaciones
def filtrar_operaciones(columna, valor):
    filtered_df = df[df[columna] == valor]
    return filtered_df

# Función para obtener datos del mercado (ejemplo con una API pública)
def obtener_datos_mercado():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return data

# Interfaz de Streamlit
st.title("Registro de Operaciones de Trading")

# Formulario para registrar una operación
tipo_opcion = st.selectbox("Tipo de Opción", ['Compra', 'Venta'])
par_divisas = st.text_input("Par de Divisas (Ej: EUR/USD)")
monto_invertido = st.number_input("Monto Invertido", min_value=0)
resultado = st.selectbox("Resultado", ['Ganancia', 'Pérdida'])
ganancia_perdida = st.number_input("Ganancia/Pérdida (en USD)")

# Botón para registrar la operación
if st.button("Registrar Operación"):
    registrar_operacion(tipo_opcion, par_divisas, monto_invertido, resultado, ganancia_perdida)

# Mostrar las operaciones registradas
if st.checkbox("Mostrar todas las operaciones"):
    st.write(df)

# Filtro de operaciones
st.subheader("Filtrar Operaciones")
filtro_columna = st.selectbox("Filtrar por", df.columns)
filtro_valor = st.text_input("Valor del filtro")
if st.button("Filtrar"):
    if filtro_valor:
        filtered_df = filtrar_operaciones(filtro_columna, filtro_valor)
        st.write(filtered_df)
    else:
        st.warning("Por favor ingresa un valor para filtrar.")

# Gráfico de Ganancias/Pérdidas
if not df.empty:
    st.subheader("Evolución de Ganancias/Pérdidas")
    fig, ax = plt.subplots()
    ax.plot(df['Fecha'], df['Ganancia/Pérdida'], marker='o', linestyle='-', color='b', label='Ganancia/Pérdida')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ganancia/Pérdida (USD)')
    ax.set_title('Evolución de las Ganancias y Pérdidas')
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Gráfico de Distribución de Ganancias/Pérdidas
if not df.empty:
    st.subheader("Distribución de Ganancias y Pérdidas")
    resultado_counts = df['Resultado'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(resultado_counts.index, resultado_counts.values, color=['green', 'red'])
    ax.set_xlabel('Resultado')
    ax.set_ylabel('Cantidad de Operaciones')
    ax.set_title('Distribución de Ganancias y Pérdidas')
    st.pyplot(fig)

# Gráfico de Tendencia de Porcentaje de Ganancia/Pérdida
if not df.empty:
    st.subheader("Tendencia de Porcentaje de Ganancia/Pérdida")
    fig, ax = plt.subplots()
    ax.plot(df['Fecha'], df['Porcentaje de Ganancia/Pérdida'], marker='o', linestyle='-', color='orange', label='Porcentaje de Ganancia/Pérdida')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Porcentaje (%)')
    ax.set_title('Tendencia del Porcentaje de Ganancia/Pérdida')
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Rentabilidad Total
if not df.empty:
    st.subheader("Rentabilidad Total")
    total_ganancia = df[df['Resultado'] == 'Ganancia']['Ganancia/Pérdida'].sum()
    total_perdida = df[df['Resultado'] == 'Pérdida']['Ganancia/Pérdida'].sum()
    rentabilidad_total = total_ganancia + total_perdida
    rentabilidad_total_porcentaje = (rentabilidad_total / df['Monto Invertido'].sum()) * 100 if df['Monto Invertido'].sum() != 0 else 0
    
    st.write(f"**Rentabilidad Total en USD**: {rentabilidad_total:.2f} USD")
    st.write(f"**Rentabilidad Total (%)**: {rentabilidad_total_porcentaje:.2f} %")

# Análisis de Estrategias
st.subheader("Análisis de Estrategias")
estrategia = st.selectbox("Seleccionar Estrategia", ['Compra', 'Venta'])

if estrategia:
    df_estrategia = df[df['Tipo de Opción'] == estrategia]
    total_ganancia_estrategia = df_estrategia[df_estrategia['Resultado'] == 'Ganancia']['Ganancia/Pérdida'].sum()
    total_perdida_estrategia = df_estrategia[df_estrategia['Resultado'] == 'Pérdida']['Ganancia/Pérdida'].sum()
    st.write(f"**Ganancia Total con {estrategia}**: {total_ganancia_estrategia:.2f} USD")
    st.write(f"**Pérdida Total con {estrategia}**: {total_perdida_estrategia:.2f} USD")

# Buscar Operaciones
st.subheader("Buscar Operaciones")
busqueda = st.text_input("Buscar por palabra clave (Ej: EUR/USD, Compra)")

if busqueda:
    busqueda_df = df[df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]
    st.write(busqueda_df)

# Exportar a CSV
st.subheader("Exportar Operaciones a CSV")
if st.button("Exportar"):
    df.to_csv('registro_operaciones_exportado.csv', index=False)
    st.success("Operaciones exportadas exitosamente.")

# Visualización de Riesgo/Beneficio
if not df.empty:
    st.subheader("Riesgo/Beneficio de las Operaciones")
    df['Riesgo/Beneficio'] = df['Ganancia/Pérdida'] / df['Monto Invertido']
    fig, ax = plt.subplots()
    ax.scatter(df['Monto Invertido'], df['Riesgo/Beneficio'], c='purple')
    ax.set_xlabel('Monto Invertido (USD)')
    ax.set_ylabel('Riesgo/Beneficio')
    ax.set_title('Análisis de Riesgo/Beneficio')
    st.pyplot(fig)

# Objetivos de Ganancia/Pérdida
objetivo_ganancia = st.number_input("Objetivo de Ganancia (USD)", min_value=0)
objetivo_perdida = st.number_input("Objetivo de Pérdida (USD)", min_value=0)

if not df.empty:
    total_ganancia = df[df['Resultado'] == 'Ganancia']['Ganancia/Pérdida'].sum()
    total_perdida = df[df['Resultado'] == 'Pérdida']['Ganancia/Pérdida'].sum()

    if total_ganancia >= objetivo_ganancia:
        st.success(f"¡Objetivo de Ganancia alcanzado! Total Ganancia: {total_ganancia:.2f} USD")
    if total_perdida <= -objetivo_perdida:
        st.warning(f"¡Objetivo de Pérdida alcanzado! Total Pérdida: {total_perdida:.2f} USD")
