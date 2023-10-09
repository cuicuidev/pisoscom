#Importamos las librerias necesarias.
import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.express as px
from streamlit_lottie import st_lottie  #Libreria necesaria para trabajar con lotties archivos json animados
import requests
from streamlit_option_menu import option_menu    #Libreria necesaria para trabajar con lotties archivos json animados
from datetime import date,datetime

#Importamos funciones de codigo en otros archivos
from intro import introduccion
from eda import eda1
from Modelos import Modelos1
from Autores import Autores

# Cargamos los DataFrames necesarios para el proyecto. Tengo todos los del EDA.


df_precios = pd.read_csv("DF/Precios por mes.csv")
df_demanda_nacional = pd.read_csv('DF/demanda_nacional.csv')
df_demanda_comunidades = pd.read_csv('DF/demanda_comunidades.csv')
df_intercambio= pd.read_csv('DF/intercambio.csv')
df_ipc = pd.read_excel("DF/IPC energía - Eurostat.xlsx", sheet_name = "Sheet 2")
df_emis_plt = pd.read_csv('DF/emis_plt_eda.csv')
df_gen_plt_eda = pd.read_csv('DF/gen_plt_eda.csv')
df_pred_dem= pd.read_csv('DF/Prediccion Demanda Nacional - 1 step.csv')
df_pred_prec=pd.read_csv('DF/Predicciones a futuro de precios (abril 2023 a agosto 2024).csv')



#Creamos el marco de trabajo de Streamlit.

def main():

    st.set_page_config(
    page_title="MODELOS REE",
    page_icon="⚡️",
    )

    # Creamos un MENÚ.
    opcion=st.sidebar.selectbox("Menú", 
                                ["INTRODUCCIÓN",
                                 "ANALISIS EXPLORATORIO DE LOS DATOS",
                                 "MODELOS DE PREDICCIÓN",
                                 "RESULTADOS Y CONCLUSIONES",
                                 "AUTORES"])
   
    #################################### INTRODUCCÓN ################################################
    #################################################################################################
    #################################################################################################

    if opcion == 'INTRODUCCIÓN':
        introduccion()

    #################################### EDA (Exploratory Data Analisys) ###########################
    ################################################################################################
    ################################################################################################

    elif opcion == 'ANALISIS EXPLORATORIO DE LOS DATOS':
        
        eda1(df_demanda_nacional     = df_demanda_nacional.copy(),
            df_demanda_comunidades  = df_demanda_comunidades.copy(),
            df_precios              = df_precios.copy(),
            df_emis_plt             = df_emis_plt.copy(),
            df_gen_plt_eda          = df_gen_plt_eda.copy()
            )

    #################################### MODELOS DE PREDICCIÓN #####################################
    ################################################################################################
    ################################################################################################
    
    elif opcion == 'MODELOS DE PREDICCIÓN':
        Modelos1()

    ##################################### RESULTADOS Y CONCLUSIONES ################################
    ################################################################################################
    ################################################################################################
    
    elif opcion == 'RESULTADOS Y CONCLUSIONES':
        st.markdown('<h1 style="font-size: 40px; text-align: justify;">RESULTADOS Y CONCLUSIONES</h1>', unsafe_allow_html=True) 

        st_lottie(requests.get("https://lottie.host/7f675139-8c7f-4cd0-93c0-0d1831dcfdc6/Kb96HXJOD7.json").json(), height=250, key="model")
        
        # Texto
        st.write('<div style="text-align: justify;"> El mejor modelo para ambos casos son las Redes Neuronales\
                                 con unas métricas de r2 de 0,94 para el caso de la demanda y 0,92 en el caso de los precios. \
                                    En este apartado puedes seleccionar en los filtros el rango de fechas que deses observar. \
                                   \
                                </div>', unsafe_allow_html=True) 
        
        
        df = df_pred_dem
        # from_ = st.slider('Desde', fecha_inicio, fecha_fin, fecha_fin	, key = 'generación_from')
        # to = st.slider('Hasta', from_, fecha_fin, fecha_fin, key = 'generación_to')

        fecha_min=datetime.strptime(df["Fechas"].min(),"%Y-%m-%d").date()
        fecha_max=datetime.strptime(df["Fechas"].max(),"%Y-%m-%d").date()
        # st.write(fecha_min)
        # st.write(fecha_max)
        fecha_inicio = st.date_input("Fecha inicio", value = fecha_min,  min_value = fecha_min, max_value = fecha_max)
        fecha_fin = st.date_input("Fecha fin", value = fecha_max, min_value = fecha_min, max_value = fecha_max)

        df["Fechas"] = df["Fechas"].apply(lambda x : datetime.strptime(x,"%Y-%m-%d").date())
        demanda= df[(df["Fechas"] >= fecha_inicio) & (df["Fechas"] <= fecha_fin)]


        
        # Gráficas predicciones.
        # Demanda
        fig24=px.line(data_frame = demanda ,
                    x = "Fechas",
                    y =  "Predicciones",  
                    title = "Predicción demanda energética nacional Redes Neuronales",
                    labels={"Fechas": "Ultimo año", "Predicciones": "Mw/h"})     

        st.plotly_chart(figure_or_data = fig24, use_container_width = True)

        #Precios

        df1 = df_pred_prec
        
        fecha_min1=datetime.strptime(df1["Fecha"].min(),"%Y-%m-%d").date()
        fecha_max1=datetime.strptime(df1["Fecha"].max(),"%Y-%m-%d").date()
        # st.write(fecha_min)
        # st.write(fecha_max)
        fecha_inicio1 = st.date_input("Fecha inicio", value = fecha_min1,  min_value = fecha_min1, max_value = fecha_max1)
        fecha_fin1 = st.date_input("Fecha fin", value = fecha_max1, min_value = fecha_min1, max_value = fecha_max1)

        df1["Fecha"] = df1["Fecha"].apply(lambda x : datetime.strptime(x,"%Y-%m-%d").date())
        precios= df1[(df1["Fecha"] >= fecha_inicio1) & (df1["Fecha"] <= fecha_fin1)]


        fig25 = px.line(data_frame = precios,
                    x = "Fecha",
                    y =  "Predicciones",  
                    title = "Predicción precios mercado eléctrico con Redes Neuronales",
                    labels={"Fecha": "Ultimo año", "Predicciones": "€/Mw/h"})    

        st.plotly_chart(figure_or_data = fig25, use_container_width = True)

        st.write('<div style="text-align: justify;"> Puedes consultar el código realizado para conseguir estos resultados en el siguiente enlace de githhub\
                                 . \
                                   \
                                </div>', unsafe_allow_html=True) 
        
        st.markdown("[![GuitHub](<https://img.icons8.com/material-outlined/48/000000/github.png>)](<https://github.com/Dande8719/Predicci-n-de-series-temporales-con-Redes-Neuronales-Datos-REE->)")

    elif opcion == 'AUTORES':  
        Autores()

    ############################# CARGAMOS IMÁGENES Y PIE  DE PÁGINA #######################
    ###############################################################################################
    ###############################################################################################    

    st.markdown("***")
    col1, col2, col3 = st.columns([2, 3, 1])
    #Introcucimos imagenes principales para la página.
    
    
    
    ############################# CERRAMOS ESTRUCTURA DEL MODELO ########################
    ############################################################################################
    ############################################################################################

if __name__ == "__main__":
    main()