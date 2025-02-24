import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Título de la aplicación
st.title('Registro de Operaciones de Trading')

# Toma la entrada del usuario para los detalles de la operación
with st.form("trading_form"):
    st.header("Detalles de la Operación")
    fecha = st.date_input("Fecha", datetime.date.today())
    hora = st.time_input("Hora", datetime.datetime.now().time())
    tipo_operacion = st.selectbox("Tipo de operación", ["Compra", "Venta"])
    cantidad = st.number_input("Cantidad", min_value=1)
    precio = st.number_input("Precio de la operación", min_value=0.01)
    comision = st.number_input("Comisión (en %)", min_value=0.0, max_value=100.0, value=0.0)
    
    submit_button = st.form_submit_button(label="Registrar Operación")

# Si el formulario es enviado
if submit_button:
    # Calcular el total con la comisión
    total = cantidad * precio
    comision_total = (comision / 100) * total
    total_con_comision = total + comision_total
    
    # Crear un DataFrame con los detalles de la operación
    operacion = {
        'Fecha': fecha,
        'Hora': hora,
        'Tipo': tipo_operacion,
        'Cantidad': cantidad,
        'Precio': precio,
        'Comisión': comision,
        'Total': total_con_comision
    }
    
    # Mostrar los detalles de la operación
    st.subheader("Detalles de la Operación Registrada")
    st.write(operacion)

    # Guardar los detalles en un archivo CSV
    try:
        # Leer el archivo CSV existente (si existe)
        df = pd.read_csv('operaciones_trading.csv')
    except FileNotFoundError:
        # Si el archivo no existe, crear un nuevo DataFrame
        df = pd.DataFrame(columns=['Fecha', 'Hora', 'Tipo', 'Cantidad', 'Precio', 'Comisión', 'Total'])
    
    # Agregar la nueva operación al DataFrame
    df = df.append(operacion, ignore_index=True)
    
    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv('operaciones_trading.csv', index=False)
    st.success("Operación registrada exitosamente.")

# Mostrar todas las operaciones registradas
st.header("Historial de Operaciones")
try:
    operaciones_df = pd.read_csv('operaciones_trading.csv')
    st.write(operaciones_df)
    
    # Calcular los porcentajes de ganancia/pérdida
    operaciones_df['Ganancia/Pérdida'] = 0
    for index, row in operaciones_df.iterrows():
        if row['Tipo'] == 'Venta':
            # Buscar la compra correspondiente para la venta
            compra = operaciones_df[(operaciones_df['Tipo'] == 'Compra') & (operaciones_df['Fecha'] <= row['Fech
