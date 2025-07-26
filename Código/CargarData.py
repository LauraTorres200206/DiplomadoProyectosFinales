import streamlit as st
import pandas as pd
import geopandas as gpd
import requests
import os

# --------------------------------------------
# Cargar datos desde API
# --------------------------------------------
def Cargar_API(limit: int = 50000) -> pd.DataFrame:
    api_url = f"https://www.datos.gov.co/resource/nudc-7mev.json?$limit={limit}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error al cargar datos desde la API: {e}")
        return pd.DataFrame()

# --------------------------------------------
# Cargar archivo Excel local
# --------------------------------------------
def cargar_excel_local(ruta: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(ruta)
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo de Excel: {e}")
        return pd.DataFrame()

# --------------------------------------------
# Cargar archivo SHP local
# --------------------------------------------
def cargar_shapefile_local(ruta: str) -> gpd.GeoDataFrame:
    try:
        gdf = gpd.read_file(ruta)
        return gdf
    except Exception as e:
        st.error(f"Error al leer el archivo SHP: {e}")
        return gpd.GeoDataFrame()

# --------------------------------------------
# Interfaz de carga
# --------------------------------------------
def Mostrar_Data():
    st.title("📊 Carga de Datos")

    # Botón y carga de datos API
    if st.button("🔄 Cargar datos educativos (API)"):
        with st.spinner("Cargando datos educativos..."):
            df_api = Cargar_API()
        if not df_api.empty:
            st.session_state['df_api'] = df_api
            st.success(f"API cargada con {df_api.shape[0]} filas.")
            st.dataframe(df_api.head())
    
    # Mostrar si ya existe
    if 'df_api' in st.session_state:
        st.subheader("✅ Datos Educativos🎓")
        st.dataframe(st.session_state['df_api'].head())

    # Botón y carga datos de población (Excel)
    if st.button("📥👨‍👩‍👧‍👦 Cargar datos poblacionales (Excel)"):
        ruta_excel = "C:\\Users\\L e n o v o\\Diplomado\\Datos\\Poblacion2005-2035.xlsx"
        with st.spinner("Cargando datos poblacionales..."):
            df_pob = cargar_excel_local(ruta_excel)
        if not df_pob.empty:
            st.session_state['df_pob'] = df_pob
            st.success(f"Data cargada con {df_pob.shape[0]} filas.")
            st.dataframe(df_pob.head())
    