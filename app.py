import streamlit as st
import pandas as pd
from datetime import datetime

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

# Filtrar operaciones
st.subheader("Filtrar Operaciones")
filtro_columna = st.selectbox("Filtrar por", df.columns)
filtro_valor = st.text_input("Valor del filtro")
if st.button("Filtrar"):
    if filtro_valor:
        filtered_df = filtrar_operaciones(filtro_columna, filtro_valor)
        st.write(filtered_df)
    else:
        st.warning("Por favor ingresa un valor para filtrar.")
