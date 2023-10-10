import streamlit as st
from streamlit_lottie import st_lottie
import requests

def app():

    
    st.markdown('<h1 style="font-size: 40px; text-align: justify;">PROPERTY PRICE PREDICTOR</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 20px; text-align: justify;">La Caculadora del precio de mercado de la vivienda</h1>', unsafe_allow_html=True)
    
    st_lottie(requests.get("https://lottie.host/ecc8a4d4-40c8-44ce-933f-1ca4c3041220/0XipcxeEJL.json").json(), height=250, key="Into1")
    

    Ciudad=st.sidebar.selectbox("Elige tu ciudad", 
                                ["MADRID",
                                 "A CORUÑA"])
    
    if Ciudad == "MADRID":

        st.write('<div style="text-align: justify;"> Escoge las características de tu vivienda en Madrid para obtener un precio .</div>', unsafe_allow_html=True)  
        # Slider de selección m2.
        st.slider("Selecciona los metros cuadrados de tu vivienda:", min_value=0, max_value=300, value=75, step=1)    
        
        # Slider de selección habitaciones.
        st.slider("Selecciona las habitaciones de tu vivienda:", min_value=0, max_value=5, value=2, step=1)    
        
        # Slider de selección baños.
        st.slider("Selecciona los baños de tu vivienda:", min_value=0, max_value=3, value=2, step=1)

        # Slider de selección Conservación.
        Conservacion= [' A estrenar', ' En buen estado', ' A reformar', ' Reformado']
        st.selectbox("Selecciona el estado de conservación de la vivienda:", Conservacion)

        # Slider de selección Clasificación.
        Clasificacion= ['En trámite','No indicado','Disponible','Pendiente de completar','Exento']
        st.selectbox("Selecciona si tiene el certificado energético:", Clasificacion)

    elif Ciudad == "A CORUÑA":

        st.write('<div style="text-align: justify;"> Escoge las características de tu vivienda en A Coruña para obtener un precio .</div>', unsafe_allow_html=True)  
        # Slider de selección m2.
        st.slider("Selecciona los metros cuadrados de tu vivienda:", min_value=0, max_value=300, value=75, step=1)    
        
        # Slider de selección habitaciones.
        st.slider("Selecciona las habitaciones de tu vivienda:", min_value=0, max_value=5, value=2, step=1)    
        
        # Slider de selección baños.
        st.slider("Selecciona los baños de tu vivienda:", min_value=0, max_value=3, value=2, step=1)  
    
    

if __name__ == "__app__":
    app()