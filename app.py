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
    
    print("Operación registrada con éxito!")

# Función para filtrar las operaciones
def filtrar_operaciones(columna, valor):
    filtered_df = df[df[columna] == valor]
    return filtered_df

# Ejemplo de uso
registrar_operacion('Compra', 'EUR/USD', 100, 'Ganancia', 15)
registrar_operacion('Venta', 'GBP/USD', 200, 'Pérdida', -25)

# Filtrar por tipo de opción
print(filtrar_operaciones('Tipo de Opción', 'Compra'))

# Filtrar por resultado
print(filtrar_operaciones('Resultado', 'Ganancia'))
