import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

def Mostrar_Mapa():
    st.header("🗺️ Mapa Interactivo por Departamento")

    if 'df_hechos' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    TablaHechos = st.session_state['df_hechos']
    Dimmunicipio = st.session_state['Dimmunicipio']
    DimDepartamento = st.session_state['DimDepartamento']
    DimTiempo = st.session_state['DimTiempo']

    df = TablaHechos.merge(DimDepartamento, on='ID_Departamento') \
                    .merge(DimTiempo, on='ID_año') \
                    .merge(Dimmunicipio, on='ID_municipio')

    metricas = {
        'Cobertura Neta (%)': 'cobertura_neta',
        'Cobertura Bruta (%)': 'cobertura_bruta',
        'Tasa de Matriculación 5-16 (%)': 'tasa_matriculacion_5_16',
        'Repitencia (%)': 'repitencia',
        'Aprobación (%)': 'aprobaci_n',
        'Reprobacion (%)': 'reprobacion'
    }

    metrica_label = st.selectbox("Selecciona la métrica", list(metricas.keys()))
    metrica_col = metricas[metrica_label]

    años = sorted(df['año'].unique())
    año_sel = st.selectbox("Selecciona el año", años, index=len(años)-1)

    df_filtrado = df[df['año'] == año_sel]
    resumen = (
        df_filtrado
        .groupby('codigo_departamento')[metrica_col]
        .mean()
        .reset_index()
        .rename(columns={'codigo_departamento': 'codigo_departamento'})
    )
    resumen['codigo_departamento'] = resumen['codigo_departamento'].astype(str)

    # ===============================
    # Leer archivo SHP local de departamentos
    # ===============================
    try:
        gdf = gpd.read_file("C:/Users/L e n o v o/Diplomado/Datos/MGN_ANM_DPTOS.shp")
    except Exception as e:
        st.error(f"❌ Error al leer el archivo .shp: {e}")
        return

    codigo_col = "DPTO_CCDGO"

    gdf[codigo_col] = gdf[codigo_col].astype(str)
    resumen[codigo_col] = resumen["codigo_departamento"]

    gdf_merged = gdf.merge(resumen, on=codigo_col, how="left")

    # ===============================
    # Crear el mapa
    # ===============================
    m = folium.Map(location=[4.6, -74.1], zoom_start=5, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data=gdf_merged,
        name="choropleth",
        data=gdf_merged,
        columns=[codigo_col, metrica_col],
        key_on=f"feature.properties.{codigo_col}",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color="gray",
        legend_name=f"{metrica_label} - {año_sel}",
        highlight=True
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st.subheader(f"🧭 {metrica_label} por Departamento - {año_sel}")
    st_folium(m, width=750, height=550)
