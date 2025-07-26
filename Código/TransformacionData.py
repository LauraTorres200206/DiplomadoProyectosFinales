import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Colores oficiales Universidad Santo Tomás
UST_BLUE = "#002855"
UST_YELLOW = "#FFD100"
UST_GRAY = "#F5F5F5"
UST_WHITE = "#FFFFFF"

# Estilo general
st.markdown(f"""
    <style>
    .main {{
        background-color: {UST_GRAY};
    }}
    .stApp {{
        background-color: {UST_WHITE};
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }}
    .stButton>button {{
        background-color: {UST_YELLOW};
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
    }}
    .stDownloadButton>button {{
        background-color: {UST_BLUE};
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: bold;
        background-color: {UST_WHITE};
        color: {UST_BLUE};
        border-radius: 6px 6px 0 0;
        border: 1px solid #CCC;
    }}
    </style>
""", unsafe_allow_html=True)
def ajuste_cod_dpto(codigo):
    codigo = str(codigo)
    if len(codigo)==1:
        codigo = '0' + codigo
    return codigo
def ajuste_cod_mpo(codigo):
    codigo = str(codigo)
    if len(codigo)==4:
        codigo = '0' + codigo
    return codigo
def Mostrar_transformacion():
    st.title("📊 Dashboard Educativo: Modelo Estrella")

    if 'df_api' not in st.session_state:
        st.warning("🔺 Primero debes cargar los datos desde la pestaña correspondiente.")
        return
    if 'df_pob' not in st.session_state:
        st.warning("🔺 Primero debes cargar los datos de poblacion desde la pestaña correspondiente.")
        return
    df = st.session_state['df_api'].copy()
    dfPob = st.session_state['df_pob'].copy()
    st.markdown("""
    ### 🛠️ Etapas del Flujo de Trabajo
    1. **Limpieza de datos**
    2. **Construcción de dimensiones**
    3. **Modelo estrella y tabla de hechos**
    4. **Visualización y métricas clave**
    5. **Descarga y resumen detallado**
    """)
    st.markdown("---")
    st.subheader("1️⃣ Limpieza y Validación de Datos")
    dfPob = dfPob.rename(columns={
    'DP': 'codigo_departamento',
    'DPNOM': 'departamento',
    'MPIO': 'codigo_municipio',
    'DPMP': 'municipio',
    'AÑO': 'año'})
    df = df.rename(columns={
    'c_digo_departamento': 'codigo_departamento',
    'departamento': 'departamento',
    'c_digo_municipio': 'codigo_municipio',
    'municipio': 'municipio',
    'c_digo_etc': 'codigo_etc',
    'etc': 'etc',
    'a_o': 'año',
    'poblaci_n_5_16': 'poblacion_5_16',
    'deserci_n_transici_n': 'desercion_transicion',
    'deserci_n_media': 'desercion_media',
    'deserci_n_secundaria': 'desercion_secundaria',
    'deserci_n_primaria': 'desercion_primaria',
    'repitencia_transici_n': 'repitencia_transicion',
    'repitencia_secundaria': 'repitencia_secundaria',
    'reprobaci_n_media': 'reprobacion_media',
    'repitencia_primaria': 'repitencia_primaria',
    'repitencia': 'repitencia',
    'repitencia_media': 'repitencia_media',
    'deserci_n': 'desercion',
    'reprobaci_n_secundaria': 'reprobacion_secundaria',
    'cobertura_bruta_media': 'cobertura_bruta_media',
    'tasa_matriculaci_n_5_16': 'tasa_matriculacion_5_16',
    'cobertura_neta': 'cobertura_neta',
    'cobertura_bruta_transici_n': 'cobertura_bruta_transicion',
    'reprobaci_n_primaria': 'reprobacion_primaria',
    'cobertura_bruta_primaria': 'cobertura_bruta_primaria',
    'cobertura_neta_primaria': 'cobertura_neta_primaria',
    'reprobaci_n': 'reprobacion',
    'aprobaci_n_transici_n': 'aprobacion_transicion',
    'reprobaci_n_transici_n': 'reprobacion_transicion',
    'aprobaci_n_media': 'aprobacion_media',
    'cobertura_bruta_secundaria': 'cobertura_bruta_secundaria',
    'cobertura_neta_secundaria': 'cobertura_neta_secundaria',
    'cobertura_neta_media': 'cobertura_neta_media',
    'cobertura_bruta': 'cobertura_bruta',
    'cobertura_neta_transici_n': 'cobertura_neta_transicion',
    'aprobaci_n_secundaria': 'aprobacion_secundaria',
    'tama_o_promedio_de_grupo': 'tamano_promedio_grupo',
    'sedes_conectadas_a_internet': 'sedes_conectadas_internet'})
    df['codigo_departamento'] = df['codigo_departamento'].apply(ajuste_cod_dpto)
    df['codigo_municipio'] = df['codigo_municipio'].apply(ajuste_cod_mpo)
    dfPob['codigo_departamento']= dfPob['codigo_departamento'].apply(ajuste_cod_dpto)
    dfPob['codigo_municipio'] = dfPob['codigo_municipio'].apply(ajuste_cod_mpo)
    dfPob['año'] = pd.to_numeric(dfPob['año'], errors='coerce')
    df['año'] = pd.to_numeric(df['año'], errors='coerce')
    ColumnasConvertir = df.columns[7:41]
    for col in ColumnasConvertir:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df[df.isna().sum(axis=1) <= 10]
    ColumnsImputar = [
    'desercion_transicion', 'desercion_media', 'desercion_secundaria',
    'desercion_primaria', 'repitencia_transicion', 'repitencia_secundaria',
    'reprobacion_media', 'repitencia_primaria', 'repitencia', 'repitencia_media',
    'desercion', 'reprobacion_secundaria', 'cobertura_bruta_media',
    'tasa_matriculacion_5_16', 'cobertura_neta', 'cobertura_bruta_transicion',
    'reprobacion_primaria', 'cobertura_bruta_primaria', 'cobertura_neta_primaria',
    'reprobacion', 'aprobacion_transicion', 'reprobacion_transicion',
    'aprobacion_media', 'cobertura_bruta_secundaria', 'cobertura_neta_secundaria',
    'cobertura_neta_media', 'cobertura_bruta', 'cobertura_neta_transicion',
    'aprobacion_secundaria']
    df_imputado = df.copy()
    for col in ColumnsImputar:
        df_imputado[col] = df_imputado.groupby('codigo_departamento')[col].transform(
        lambda x: x.fillna(x.median(skipna=True))
        ) # Imputamos con la mediana por departamento para que no nos afecte tanto la distribución
    columnas_omitir = ['tamano_promedio_grupo', 'sedes_conectadas_internet']
    Data = df_imputado.drop(columns=columnas_omitir)
    tabla_deptos = (
        Data
        .query("departamento != 'NACIONAL'")
        [['codigo_departamento','departamento']]
        .drop_duplicates()
        .groupby('codigo_departamento')
        .sample(n=1, random_state=1)
        .reset_index()
        .drop(columns= 'index')
    )
    Data = (
        Data
        .query("departamento != 'NACIONAL'")
        .drop(columns = 'departamento')
        .merge(tabla_deptos, on = 'codigo_departamento', how = 'left')
    )
    tabla_mpios = (
        Data
        [['codigo_municipio','municipio']]
        .drop_duplicates()
        .groupby('codigo_municipio')
        .sample(n=1, random_state=1)
        .reset_index()
        .drop(columns= 'index')
    )
    Data = (
        Data
        .drop(columns = 'municipio')
        .merge(tabla_mpios, on = 'codigo_municipio', how = 'left')
    )    
    
    col1, col2 = st.columns(2)
    col1.metric("Registros originales", len(st.session_state['df_api']))
    col2.metric("Registros después de limpieza e imputación", len(Data))
    st.markdown("---")
    st.subheader("2️⃣ Dimensiones del Modelo Estrella")
    def crear_dimension(df, cols, nombre, sort_col=None):
        dim = df[cols].drop_duplicates()
        if sort_col:
            dim = dim.sort_values(by=sort_col)
        dim = dim.reset_index(drop=True)
        dim[f"ID_{nombre}"] = dim.index + 1
        return dim[[f"ID_{nombre}"] + cols]

    DimTiempo = Data[['año']].drop_duplicates().reset_index(drop=True)
    DimTiempo['ID_año'] = DimTiempo.index + 1  
    Dimmunicipio = Data[['codigo_municipio', 'municipio']].drop_duplicates().reset_index(drop=True)
    Dimmunicipio['ID_municipio'] = Dimmunicipio.index + 1  
    DimDepartamento = Data[['codigo_departamento', 'departamento']].drop_duplicates().reset_index(drop=True)
    DimDepartamento['ID_Departamento'] = DimDepartamento.index + 1  
    DimTiempoPob = dfPob[['año']].drop_duplicates().reset_index(drop=True)
    DimTiempoPob['ID_año'] = DimTiempoPob.index + 1 

    col3, col4, col5 = st.columns(3)
    col3.metric("Dimensión Tiempo", len(DimTiempo))
    col4.metric("Dimensión Departamento", len(DimDepartamento))
    col5.metric("Dimensión Municipio", len(Dimmunicipio))
  

    st.markdown("---")
    st.subheader("Tabla de Hechos")
    df_hechos = Data.copy()
    df_hechos = df_hechos.merge(Dimmunicipio, on=['codigo_municipio', 'municipio'], how='left')
    df_hechos = df_hechos.merge(DimDepartamento, on=['codigo_departamento', 'departamento'], how='left')
    df_hechos = df_hechos.merge(DimTiempo, on=['año'], how='left')
    ColumnasFinales = df_hechos.columns[5:42].tolist()
    TablaHechos = df_hechos[ColumnasFinales].copy()
    st.success(f"✅ Tabla de hechos construida con {len(TablaHechos):,} registros.")
    st.session_state['df_hechos'] = TablaHechos
    st.session_state['Dimmunicipio'] = Dimmunicipio
    st.session_state['DimDepartamento'] = DimDepartamento
    st.session_state['DimTiempo'] = DimTiempo
    Poblacion=dfPob.copy()
    Poblacion = Poblacion.merge(DimTiempo, on='año', how='inner')
    Poblacion = Poblacion.merge(DimDepartamento, on=['codigo_departamento','departamento'], how='inner')
    st.session_state['Poblacion'] = Poblacion
    st.markdown("---")
    st.subheader("3️⃣ Visualización y métricas clave: En la siguiente pestaña")
    df = TablaHechos.merge(DimDepartamento, on='ID_Departamento').merge(DimTiempo, on='ID_año').merge(Dimmunicipio, on='ID_municipio')

    st.sidebar.title("Filtros")
    año = st.sidebar.selectbox("Selecciona un año", sorted(df["año"].unique(), reverse=True))
    departamento = st.sidebar.selectbox("Selecciona un departamento", sorted(df["departamento_x"].dropna().unique()))
    municipios = df[df["departamento_x"] == departamento]["municipio_x"].dropna().unique()
    municipio = st.sidebar.selectbox("Selecciona un municipio", sorted(municipios))
    st.session_state['año_filtrado'] = año
    st.session_state['departamento_filtrado'] = departamento
    st.session_state['municipio_filtrado'] = municipio
# Filtrar datos según selección
    df_filtrado = df[(df["año"] == año) & 
                 (df["departamento_x"] == departamento) & 
                 (df["municipio_x"] == municipio)]

# --- MÉTRICAS ---
    st.subheader(f"📊 Indicadores clave - {municipio}, {año}")
    if not df_filtrado.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Cobertura Neta", f"{df_filtrado['cobertura_neta'].values[0]:.2f}%")
        col2.metric("Tasa Matriculación 5-16", f"{df_filtrado['tasa_matriculacion_5_16'].values[0]:.2f}%")
        col3.metric("Deserción", f"{df_filtrado['desercion'].values[0]:.2f}%")

        col4, col5= st.columns(2)
        col4.metric("Aprobación", f"{df_filtrado['aprobaci_n'].values[0]:.2f}%")
        col5.metric("Reprobación", f"{df_filtrado['reprobacion'].values[0]:.2f}%")
    else:
        st.warning("No se encontraron datos para la selección dada.")

    st.markdown("---")
    st.subheader("4️⃣ Vista y Descarga de la Tabla de Hechos")

    st.dataframe(TablaHechos.head(50))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        TablaHechos.to_excel(writer, index=False, sheet_name='TablaHechos')
    output.seek(0)

    st.download_button(
        label="📥 Descargar Tabla de Hechos",
        data=output,
        file_name='tabla_hechos_educacion.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    





