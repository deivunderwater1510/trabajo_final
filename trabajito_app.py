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
 