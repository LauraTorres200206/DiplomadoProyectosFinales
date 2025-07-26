import streamlit as st
from CargarData import Mostrar_Data
from TransformacionData import Mostrar_transformacion
from VisualizacionData import Mostrar_Visualizaciones
from Mapa import Mostrar_Mapa


# Crear pestañas en el cuerpo de la aplicación
tabs = st.tabs(["📥 Carga de Datos", "🔧 Transformación y Métricas", "📊 Visualizaciones", "🗺️ Mapa"])

# Mostrar contenido en cada pestaña
with tabs[0]:
    Mostrar_Data()
with tabs[1]:
    Mostrar_transformacion()
with tabs[2]:
    Mostrar_Visualizaciones()
with tabs[3]:
    Mostrar_Mapa()

