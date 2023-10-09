import streamlit as st
from streamlit_lottie import st_lottie
import requests

def introduccion():

    #st.header("MODELOS DE PREDICCIÓN DE SERIES TEMPORALES")
    st.markdown('<h1 style="font-size: 40px; text-align: justify;">MODELOS DE PREDICCIÓN PRECIOS DE VIVIENDAS</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 20px; text-align: justify;">Calculadora de precio de mercado de la vivienda en XXX. </h1>', unsafe_allow_html=True)
    
    st_lottie(requests.get("https://lottie.host/ecc8a4d4-40c8-44ce-933f-1ca4c3041220/0XipcxeEJL.json").json(), height=250, key="Into1")
    
    st.write('<div style="text-align: justify;">El objeto del siguiente proyecto es usar los diversos datos obtenidos de la API de red \
            eléctrica para predecir datos futuros usando distintos modelos de Machine y Deep Learning (SKForecast, Redes Neuronales, Prophet, Pycaret, Arima, Sarima y Fast Forward). \
            Los datos actuales de demanda y precios nos servirán para \
            entrenar estos modelos que nos permitirán predecir estas variables en un \
            rango de tiempo determinado. \
            En esta presentación web de Streamlit podrás navegar en el menú y ver los resultados \
            de cada modelo, como norma general obtendremos un \
            gráfico de entrenamiento y unos valores de precisión del modelo que nos dirán cuán bueno es el \
            mismo. En el apartado de resultados y conclusiones podrás ver las predicciones a futuro que arrojan estos modelos y escoger un rango de tiempo para analizar esta predicción  \
                \
                .</div>', unsafe_allow_html=True)
    
    

if __name__ == "__introduccion__":
    introduccion()