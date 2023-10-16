# Importamos librerias 
import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.express as px
import datetime
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from keras.models import load_model
import requests
import json
import numpy as np
from streamlit_lottie import st_lottie
import requests

#Cargamos DataFrames necesarios
df_modelos_demanda = pd.read_csv('DF/Comparacion modelos demanda.csv')
df_modelos_precios = pd.read_csv('DF/precios_plt_eda.csv')

#Cargamos función Modelos creada en Modelos.py
def Modelos1():

    #Título
    st.markdown('<h1 style="font-size: 40px; text-align: justify;">MODELOS DE PREDICCIÓN</h1>', unsafe_allow_html=True)
    #Texto
    st.write('<div style="text-align: justify;"> A continuación seleccionamos entre las distintas variables a predecir\
              para ver los resultados de los modelos usados. De todos los datos estudiados en el EDA, solo vamos a trabajar\
              con Demanda y Precios por que son con los que se obtienen mejores resultados\
                </div>', unsafe_allow_html=True)
    #Animación
    st_lottie(requests.get("https://lottie.host/de6e98d2-b4a7-45a7-b610-ddd71c68ba1f/GdIFdrWP8O.json").json(), height=250, key="Modelos")
    #Opciones selectbox
    opcion = st.selectbox('Seleccione una opción', ['DEMANDA','PRECIOS'])

    ################################################## DEMANDA ##############################################################
    if opcion == 'DEMANDA':
        #Titulo
        st.title('DEMANDA')
        #Texto
        st.write('<div style="text-align: justify;">A continuación se muestran todos los modelos aplicados al conjunto de \
                datos de demanda energética nacional. En esta figura se pueden comparar las predicciones en el 2023 \
                frente a los valores reales.\
                 Debajo de la gráfica tenemos tres botones donde podemos selecciónar\
                cada uno de los tres mejores modelos para verlos más en detalle.</div>', unsafe_allow_html=True)

        #Imprimimos gráfico con todos los modelos.
        fig1=px.line(data_frame = df_modelos_demanda,
              x = "Fechas",
              y =  df_modelos_demanda.columns[1:],
              title = "Comparación modelos de predicción")    
        fig1.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")
        st.plotly_chart(figure_or_data = fig1, use_container_width = True)

        #Creamos estructura de columnas para los botones.
        col1, col2, col3 = st.columns([1, 1, 1])

        #Creamos una serie de botones para seleccionar el tipo de modelo a aplicar.        
        if col1.button("Modelo Prophet", key="Modelo prophet"):
                
                #Figura de prophet
                fig2=px.line(data_frame = df_modelos_demanda,
                    x = "Fechas",
                    y =  df_modelos_demanda.columns[1:3],
                    title = "Comparación modelos Prophet con Test")    
                fig2.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")
                st.plotly_chart(figure_or_data = fig2, use_container_width = True)
                st.image('Foto/Predicciones Demanda Nacional - Prophet.png')

               
                #Conclusiones de prophet
                st.write('<div style="text-align: justify;">El Modelo Prophet proporciona un dataframe con la predicción futura \
                            y la incertidumbre de esos valores. A pesar de tener solo un r2=0,82 el hecho de proporcionar estos rangos de incertidumbre \
                            hace que sea muy útil frente a otros modelos.\
                                </div>', unsafe_allow_html=True)

        if col2.button("Redes Neuronales", key="REDES NEURONALES"):
                
                # Figura de Redes Neuronales
                fig3=px.line(data_frame = df_modelos_demanda,
                    x = "Fechas",
                    y =  df_modelos_demanda.columns[2:4],
                    title = "Comparación modelo Redes Neuronales")    
                fig3.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")
                st.plotly_chart(figure_or_data = fig3, use_container_width = True)

                
                # Conclusiones de Redes Neuronales
                st.write('<div style="text-align: justify;">El Modelo de Redes Neuronales que utiliza "1 Step Prediction" nos arroja una métrica de r2=0,94 presentandose como el más  \
                            preciso de los modelos estudiados en este projecto. \
                            Esto hace que se seleccione para la predicción de la demanda energética nacional del siguiente año.\
                            En el apartado Resutados y Conclusiones podremos ver dicha predicción.\
                                </div>', unsafe_allow_html=True)

        if col3.button("SKForecast (exogenas)", key="SKForecast"):

                # Figura de SKForecast    
                fig4=px.line(data_frame = df_modelos_demanda,
                    x = "Fechas",
                    y =  ["Test","Skforecast Exogenas"],  
                    title = "Comparación modelo SKForecast")    
                fig4.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")
                st.plotly_chart(figure_or_data = fig4, use_container_width = True)

                # Conclusiones SKForecast
                st.write('<div style="text-align: justify;">El Modelo SKForecast Exogenas nos arroja un r2=0,45 no siendo el mejor de los modelos\
                                La predicción sigue la tendencia de los resultados de prueba, por lo que se puede tener una visión de cómo van a variar aunque no sean del todo precisos.\
                                Esta variable del modelo SKForecast permite introducir variables exógenas, en este caso hemos decidido que tenga en cuenta los días de la semana.\
                                </div>', unsafe_allow_html=True)
   

    ################################################## PRECIOS ############################################################## 
       
    if opcion == 'PRECIOS':
        st.title('PRECIOS')

        st.write('Obtenemos los datos de precios del mercado electrico de la API de Red eléctrica de España \
                 y obtenemos una serie temporal de datos de 8 años de precios \
                 del mercado electrico en España, valores diarios en €/Mwh.')
        
        #Plot con modelos de precios
        fig5=px.line(data_frame = df_modelos_precios,
            x = 'Fechas',
            y = ['Red Neuronal', 'Precios', 'XGBoost', 'ARIMA'],
            title = 'Comparación entre los principales modelos de predicción de precios')
        fig5.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")
        st.plotly_chart(figure_or_data = fig5, use_container_width = True)

        

        #Creamos una serie de botones para seleccionar el tipo de modelo a aplicar.
        col1, col2 = st.columns([1, 1])

        if col1.button("XGBoost", key="XGBoost"):
                
                #PLot de modelos XGBoost
                fig6=px.line(data_frame = df_modelos_precios,
                    x = 'Fechas',
                    y = ['Precios', 'XGBoost'],
                    title = 'Visulización modelo XGBoost')
                
                st.plotly_chart(figure_or_data = fig6, use_container_width = True)

                #Texto de XGBoost
                st.write('<div style="text-align: justify;"> EL Modelos XGBoost nos arroja un r2=0,65 sin ser el mejor de los modelos   \
                                sigue relativamente bien la tendencia de los resultado de prueba.\
                                </div>', unsafe_allow_html=True)

                

        if col2.button("Redes neuronales", key="Redes neuronales"):
                
                #PLot Redes Neuronales.
                fig6=px.line(data_frame = df_modelos_precios,
                    x = 'Fechas',
                    y = ['Red Neuronal', 'Precios'],
                    title = 'Visualización modelo Red Neuronal')

                st.plotly_chart(figure_or_data = fig6, use_container_width = True)

                #Texto Redes neuronales.
                st.write('<div style="text-align: justify;"> El Modelo de Redes Neuronales nos arroja una métrica r2=0,92 \
                                siendo el más preciso de los analizados para la predicción de precios. \
                                </div>', unsafe_allow_html=True)



if __name__ == "__Modelos__":
    Modelos()