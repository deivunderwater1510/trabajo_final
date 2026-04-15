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
#########################################################################################################################################
Archivo = "29. Pokemon.csv"
df = pd.read_csv("29. Pokemon.csv") #cargue mi base de datos

df["Type_2"] = df["Type_2"].fillna("Ninguno") #Antes habia revisado y como no todos los pokemones tienen dos tipo, pue le dije 
# pusiera ninguno en vez de que este vacio. 


#las variables que voy a usar y de una revise si me faltaba un datico. 
vari = ["id", "HP", "Attack", "Defense", "Sp.Atk", "Sp.Def", "Speed", "Type_1", "Type_2", "Generation", "Total_Stats"] 
print(df[vari].isnull().sum())

#######################################################################################################################################
 #ahora como todo esta clean, empezamos con el dashbor

 # 3. Título principal sumado a una pequeña invitacion 
st.title("🦾 Poké-Analytics")
st.markdown("Una verdadera exploracion por el mundo de las estadisticas pokemon")

st.sidebar.header("Tipo del Pokemon")
Tipo_Pokemon = df['Type_1'].unique()
Tipos_seleccionados = st.sidebar.multiselect(
    "Selecciona tus tipos",  # pa que seleccionen el tipo del pokemon 
    options=Tipo_Pokemon, 
    default=Tipo_Pokemon[:9] # Por defecto 9 tipos
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
    default=Gen_Pokemon[:5] # Por defecto las 5
)

# Aplicar los filtros al DataFrame
df_filtrado = df[
    (df['Type_1'].isin(Tipos_seleccionados)) & 
    (df['Generation'].isin(Gen_seleccionados))
]

df_colum = df_filtrado[Estadisticas_seleccionadas]

################################################################################################################################
col1, col2,= st.columns(2)
with col1:
    st.metric(label="Total de Pokémon", value=len(df_filtrado)) #este es para que diga con cuanta muestra estamos trabajando

with col2:
    techo = df_filtrado[Estadisticas_seleccionadas].max().max()  #este para la estadistica max alcanzada, 
    st.metric(label="Poder Máximo", value=techo)             # pero siempre coloca de todas las estadisticas seleccionadas la mayor.

tab1, tab2, tab3 = st.tabs(["Estadistica por tipo pokemon","Comparaciones de las estadisticas", "Dispersiones de las estadisticas"])
#############################################################################################################################
with tab1:
    if len(Tipos_seleccionados) > 0:
        for tipo in Tipos_seleccionados:

            df_tipo_especifico = df_filtrado[df_filtrado["Type_1"] == tipo] #para que cargue la grafica del tipo filtrado
            color_map = {"Grass": "#7AC74C","Fire": "#EE8130","Water": "#6390F0","Bug": "#A6B91A","Normal": "#A8A77A","Poison": "#A33EA1","Electric": "#F7D02C","Ground": "#E2BF65", "Fairy": "#D685AD","Fighting": "#C22E28","Psychic": "#F95587","Rock": "#B6A136","Ghost": "#735797","Ice": "#96D9D6","Dragon": "#6F35FC","Dark": "#705746","Steel": "#B7B7CE","Flying": "#A98FF3"}
                          #colores para cada tipo 
            fig = px.box(
                df_tipo_especifico,
                y=Stats,                              # La grafica en general 
                color="Type_1",
                color_discrete_map=color_map,
                title=f"Distribución de Estadisticas (Solo {tipo})",
                
    )

            st.plotly_chart(fig, use_container_width=True) #que se muestre la grafica.
            st.divider()          #y dividir la pestaña por cada tipo.
###########################################################################################################################
with tab2:
    if len(Estadisticas_seleccionadas) > 0: #tiene que haber una estadistica seleccionada para poder verse
     for Stats in Estadisticas_seleccionadas:   #y que se repita para cada estadistica seleccionada
            color_map = {"Grass": "#7AC74C","Fire": "#EE8130","Water": "#6390F0","Bug": "#A6B91A","Normal": "#A8A77A","Poison": "#A33EA1","Electric": "#F7D02C","Ground": "#E2BF65", "Fairy": "#D685AD","Fighting": "#C22E28","Psychic": "#F95587","Rock": "#B6A136","Ghost": "#735797","Ice": "#96D9D6","Dragon": "#6F35FC","Dark": "#705746","Steel": "#B7B7CE","Flying": "#A98FF3"}
                     
            fig = px.box(
                df_filtrado,
                x="Type_1",
                y=Stats,                        #grafica en general 
                color="Type_1",
                color_discrete_map=color_map,
                title=f"Distribución de {Stats} por Tipo",

    )

            st.plotly_chart(fig, use_container_width=True)
            st.divider()

##########################################################################################################################
with tab3:
    if len(Estadisticas_seleccionadas) == 2: #si o si hay que seleccionar dos estadisticas
            
        color_map = {"Grass": "#7AC74C","Fire": "#EE8130","Water": "#6390F0","Bug": "#A6B91A","Normal": "#A8A77A","Poison": "#A33EA1","Electric": "#F7D02C","Ground": "#E2BF65", "Fairy": "#D685AD","Fighting": "#C22E28","Psychic": "#F95587","Rock": "#B6A136","Ghost": "#735797","Ice": "#96D9D6","Dragon": "#6F35FC","Dark": "#705746","Steel": "#B7B7CE","Flying": "#A98FF3"}

        fig_dis = px.scatter(
                df_filtrado,
                x= Estadisticas_seleccionadas [0],
                y= Estadisticas_seleccionadas [1],  #esta grafica no se repite. se interactua pero no se repite
                color="Type_1",
                color_discrete_map=color_map,
                title= "Relación entre Estadísticas de los pokemon por Tipo",
                hover_name="Name",

    )
        fig_dis.update_layout(height=750,)        #aumento de tamaño pq se veia como aplastado
    
    
        st.plotly_chart(fig_dis, use_container_width=True)
        st.divider()                                              #divido
        st.subheader("Buscador de Pokémon")  #este es el buscador

        buscador = st.text_input("Busca ese Pokemon")  #texto que va dentro del buscador 
        
        columnas_interes = ["id", "Name", "HP" ,"Attack","Defense","Sp.Atk","Sp.Def","Speed","Type_1","Type_2"]
                 #columnas relevantes para mi datafream que va aparecer
        if buscador: 
            df_mostrar = df[df['Name'].str.contains(buscador, case=False)] #va a buscar de acuerdo con el nombre del pokemon
            df_mostrar = df_mostrar[columnas_interes] #y muestra nuestras columnas de interes
        else:
            df_mostrar = df[columnas_interes]  #en caso de no poner nada aparezca el datafream que estamos usando

        st.dataframe(df_mostrar, use_container_width=True) #que se ve nuestro datafream
##################################################################################################################

