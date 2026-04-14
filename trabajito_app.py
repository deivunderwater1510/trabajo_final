# Importación de librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(
    page_title="Dashboard de Pokemones",
    page_icon="🧢",
    layout="wide"
)

Archivo = "29. Pokemon.csv"
df = pd.read_csv("29. Pokemon.csv") #cargue mi base de datos

df["Type_2"] = df["Type_2"].fillna("Ninguno") #Antes habia revisado y como no todos los pokemones tienen dos tipo, pue le dije 
# pusiera ninguno en vez de que este vacio. 


#las variables que voy a usar y de una revise si me faltaba un datico. 
vari = ["id", "HP", "Attack", "Defense", "Sp.Atk", "Sp.Def", "Speed", "Type_1", "Type_2", "Generation", "Total_Stats"] 
print(df[vari].isnull().sum())


 #ahora como todo esta clean, empezamos con el dashbor

 # 3. Título principal sumado a una pequeña invitacion 
st.title("🦾 Poké-Analytics")
st.markdown("Una verdadera exploracion por el mundo de las estadisticas pokemon")

st.sidebar.header("Tipo del Pokemon")
Tipo_Pokemon = df['Type_1'].unique()
Tipos_seleccionados = st.sidebar.multiselect(
    "Selecciona tus tipos",  # pa que seleccionen el tipo del pokemon 
    options=Tipo_Pokemon, 
    default=Tipo_Pokemon[:9] # Por defecto 9 ciudades
)
Stats = ["HP", "Attack", "Defense", "Sp.Atk", "Sp.Def", "Speed"] 


st.sidebar.header("Estadistica de tu Pokemon")
Estadisticas_seleccionadas = st.sidebar.multiselect(
    "Selecciona tus estadisticas", 
    options=Stats,     # pa que seleccionen la estadisticas que desean estudiar.
    default=Stats[:3] # Por defecto 3 estadisticas
)

st.sidebar.header("Generacion del Pokemon")
Gen_Pokemon = df['Generation'].unique()
Gen_seleccionados = st.sidebar.multiselect(
    "Elige la gen que deseas",  # pa que seleccionen el tipo del pokemon 
    options=Gen_Pokemon, 
    default=Gen_Pokemon[:5] # Por defecto las 9 
)

# Aplicar los filtros al DataFrame
df_filtrado = df[
    (df['Type_1'].isin(Tipos_seleccionados)) & 
    (df['Generation'].isin(Gen_seleccionados))
]

df_colum = df_filtrado[Estadisticas_seleccionadas]


col1, col2,= st.columns(2)
with col1:
    st.metric(label="Total de Pokémon", value=len(df_filtrado))

with col2:
    techo = df_filtrado[Estadisticas_seleccionadas].max().max()
    st.metric(label="Poder Máximo", value=techo)

tab1, tab2, tab3 = st.tabs(["Estadistica por tipo pokemon","Comparaciones de las estadisticas", "Dispersiones de las estadisticas"])

with tab1:
    if len(Tipos_seleccionados) > 0:
        for tipo in Tipos_seleccionados:

            df_tipo_especifico = df_filtrado[df_filtrado["Type_1"] == tipo]
            color_map = {"Grass": "#7AC74C","Fire": "#EE8130","Water": "#6390F0","Bug": "#A6B91A","Normal": "#A8A77A","Poison": "#A33EA1","Electric": "#F7D02C","Ground": "#E2BF65", "Fairy": "#D685AD","Fighting": "#C22E28","Psychic": "#F95587","Rock": "#B6A136","Ghost": "#735797","Ice": "#96D9D6","Dragon": "#6F35FC","Dark": "#705746","Steel": "#B7B7CE","Flying": "#A98FF3"}
                          
            fig = px.box(
                df_tipo_especifico,
                y=Stats,
                color="Type_1",
                color_discrete_map=color_map,
                title=f"Distribución de Estadisticas (Solo {tipo})",
                
    )

            st.plotly_chart(fig, use_container_width=True)
            st.divider()

with tab2:
    if len(Estadisticas_seleccionadas) > 0:
     for Stats in Estadisticas_seleccionadas:
            color_map = {"Grass": "#7AC74C","Fire": "#EE8130","Water": "#6390F0","Bug": "#A6B91A","Normal": "#A8A77A","Poison": "#A33EA1","Electric": "#F7D02C","Ground": "#E2BF65", "Fairy": "#D685AD","Fighting": "#C22E28","Psychic": "#F95587","Rock": "#B6A136","Ghost": "#735797","Ice": "#96D9D6","Dragon": "#6F35FC","Dark": "#705746","Steel": "#B7B7CE","Flying": "#A98FF3"}

            fig = px.box(
                df_filtrado,
                x="Type_1",
                y=Stats,
                color="Type_1",
                color_discrete_map=color_map,
                title=f"Distribución de {Stats} por Tipo",

    )

            st.plotly_chart(fig, use_container_width=True)
            st.divider()


with tab3:
    if len(Estadisticas_seleccionadas) > 0 < 3:
            
            color_map = {"Grass": "#7AC74C","Fire": "#EE8130","Water": "#6390F0","Bug": "#A6B91A","Normal": "#A8A77A","Poison": "#A33EA1","Electric": "#F7D02C","Ground": "#E2BF65", "Fairy": "#D685AD","Fighting": "#C22E28","Psychic": "#F95587","Rock": "#B6A136","Ghost": "#735797","Ice": "#96D9D6","Dragon": "#6F35FC","Dark": "#705746","Steel": "#B7B7CE","Flying": "#A98FF3"}
            df_corr =  df_filtrado[Estadisticas_seleccionadas]
            corr = df_corr.corr()
            
    
            fig_corr = px.imshow(
                    corr,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    title= "Relación entre Estadísticas de los pokemon por Tipo"

        )

            st.plotly_chart(fig_corr, use_container_width=True)