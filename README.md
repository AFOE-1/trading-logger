import streamlit as st
import pandas as pd
import datetime

# Inicializar sesión de datos si no existe
if 'trades' not in st.session_state:
    st.session_state.trades = []

st.title("Registro de Operaciones - Trading Binarias")

# Formulario para ingresar datos
with st.form("trade_form"):
    date = st.date_input("Fecha", datetime.date.today())
    time = st.time_input("Hora", datetime.datetime.now().time())
    asset = st.text_input("Activo")
    amount = st.number_input("Inversión", min_value=0.0, step=0.1)
    result = st.selectbox("Resultado", ["Ganada", "Perdida"])
    submit = st.form_submit_button("Agregar operación")

if submit:
    st.session_state.trades.append({
        "Fecha": date.strftime("%Y-%m-%d"),
        "Hora": time.strftime("%H:%M"),
        "Activo": asset,
        "Inversión": amount,
        "Resultado": result,
    })
    st.success("Operación registrada con éxito")

# Mostrar tabla de registros
if st.session_state.trades:
    df = pd.DataFrame(st.session_state.trades)
    st.write("### Historial de Operaciones")
    st.dataframe(df)

    # Gráfico de rendimiento
    st.write("### Rendimiento de Inversión")
    st.line_chart(df.set_index("Fecha")["Inversión"])
