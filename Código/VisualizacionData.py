import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

def Mostrar_Visualizaciones():
    st.header("📈 Visualizaciones por Departamento")

    if 'df_hechos' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    TablaHechos = st.session_state['df_hechos']
    Dimmunicipio = st.session_state['Dimmunicipio']
    DimDepartamento = st.session_state['DimDepartamento']
    DimTiempo = st.session_state['DimTiempo']
    dfPob = st.session_state['Poblacion']
  
    df = TablaHechos.merge(DimDepartamento, on='ID_Departamento') \
                    .merge(DimTiempo, on='ID_año') \
                    .merge(Dimmunicipio, on='ID_municipio')

    año_filtro = st.session_state.get('filtro_año')
    departamento_filtro = st.session_state.get('filtro_departamento')
    municipio_filtro = st.session_state.get('filtro_municipio')

    if año_filtro and departamento_filtro and municipio_filtro:
        df_filtrado = df[(df["año"] == año_filtro) & 
                         (df["departamento_x"] == departamento_filtro) & 
                         (df["municipio_x"] == municipio_filtro)]
    else:
        df_filtrado = df.copy()

    st.subheader("📈 Evolución de la cobertura neta por departamento")

    departamentos_disponibles = sorted(df_filtrado['departamento_x'].dropna().unique())
    selected_depto_1 = st.selectbox("Selecciona un departamento", departamentos_disponibles)

    df_1 = df[df['departamento_x'] == selected_depto_1]
    df_1 = df_1.groupby('año')[['tasa_matriculacion_5_16', 'cobertura_neta']].mean().reset_index()

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=df_1['año'],
        y=df_1['tasa_matriculacion_5_16'],
        name='Tasa de matriculación (5-16)',
        mode='lines+markers',
        yaxis='y1',
        line=dict(color='blue')
    ))

    fig1.add_trace(go.Scatter(
        x=df_1['año'],
        y=df_1['cobertura_neta'],
        name='Cobertura neta',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='orange')
    ))

    fig1.update_layout(
        title=f"Evolución por año - {selected_depto_1}",
        xaxis=dict(title='Año'),
        yaxis=dict(
            title=dict(text='Tasa de Matriculación (%)', font=dict(color='blue')),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title=dict(text='Cobertura Neta (%)', font=dict(color='orange')),
            tickfont=dict(color='orange'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ================================
    # SEGUNDO GRÁFICO
    # ================================
    st.subheader("📊 Serie de tiempo: Cobertura Bruta vs Repiticencia")

    selected_depto_2 = st.selectbox("Selecciona un departamento (Gráfico 2)", departamentos_disponibles, index=departamentos_disponibles.index(selected_depto_1))

    df_2 = df[df['departamento_x'] == selected_depto_2]
    df_2_grouped = df_2.groupby('año').agg({
        'cobertura_bruta': 'mean',
        'repitencia': 'mean' if 'repitencia' in df_2.columns else 'mean',
        'tasa_matriculacion_5_16': 'mean'
    }).reset_index()

    if 'repitencia' in df.columns:
        df_2_grouped['otra_metrica'] = df_2_grouped['repitencia']
        nombre_metrica = 'Repitencia'
    else:
        df_2_grouped['otra_metrica'] = df_2_grouped['tasa_matriculacion_5_16']
        nombre_metrica = 'Tasa de Matriculación (5-16)'

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=df_2_grouped['año'],
        y=df_2_grouped['cobertura_bruta'],
        name='Cobertura Bruta',
        mode='lines+markers',
        yaxis='y1',
        line=dict(color='green')
    ))

    fig2.add_trace(go.Scatter(
        x=df_2_grouped['año'],
        y=df_2_grouped['otra_metrica'],
        name=nombre_metrica,
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='purple')
    ))

    fig2.update_layout(
        title=f"Cobertura Bruta vs {nombre_metrica} - {selected_depto_2}",
        xaxis=dict(title='Año'),
        yaxis=dict(
            title=dict(text='Cobertura Bruta (%)', font=dict(color='green')),
            tickfont=dict(color='green')
        ),
        yaxis2=dict(
            title=dict(text=nombre_metrica, font=dict(color='purple')),
            tickfont=dict(color='purple'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("👶 Proporción de niños/as 5-16 años sobre la población total")
    df['departamento_x'] = df['departamento_x'].str.upper().str.strip()
    dfPob['departamento'] = dfPob['departamento'].str.upper().str.strip()
    df_edu = df.groupby(['departamento_x', 'año'], as_index=False)['poblacion_5_16'].sum()
    df_pob = dfPob.groupby(['departamento', 'año'], as_index=False)['Población'].sum()
    df_pob.rename(columns={'departamento': 'departamento_x'}, inplace=True)
    df_comparado = pd.merge(df_edu, df_pob, on=['departamento_x', 'año'], how='inner')
    df_comparado['porcentaje_5_16'] = (df_comparado['poblacion_5_16'] / df_comparado['Población']) * 100

    depto_comparado = st.selectbox("Selecciona un departamento", sorted(df_comparado['departamento_x'].unique()))

    df_graf = df_comparado[df_comparado['departamento_x'] == depto_comparado]

    fig_p5_16 = px.line(
        df_graf,
        x='año',
        y='porcentaje_5_16',
        markers=True,
        title=f"Proporción de niños 5-16 años vs población total en {depto_comparado}",
        labels={'porcentaje_5_16': '% población 5-16'}
    )

    st.plotly_chart(fig_p5_16, use_container_width=True)
