import streamlit as st
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Título de la aplicación
st.title('Clasificador Iris con RandomForest')

# Cargar el dataset Iris
st.write('## Dataset Iris')
iris = load_iris()
X = iris.data
y = iris.target

# Dividir el dataset en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear el modelo RandomForest
model = RandomForestClassifier()

# Entrenar el modelo
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Calcular la precisión
accuracy = accuracy_score(y_test, y_pred)

# Mostrar la precisión
st.write(f'## Precisión del modelo: {accuracy:.2f}')

# Interfaz para que el usuario ingrese características
st.write('### Ingresa características para predecir la especie de la flor:')
sepal_length = st.slider('Longitud del sépalo (cm)', 4.0, 8.0, 5.0)
sepal_width = st.slider('Ancho del sépalo (cm)', 2.0, 5.0, 3.0)
petal_length = st.slider('Longitud del pétalo (cm)', 1.0, 7.0, 3.5)
petal_width = st.slider('Ancho del pétalo (cm)', 0.1, 2.5, 1.0)

# Realizar la predicción con los valores ingresados
user_input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
prediction = model.predict(user_input)

# Mostrar la predicción
species = iris.target_names[prediction][0]
st.write(f'### Predicción de la especie: {species}')
