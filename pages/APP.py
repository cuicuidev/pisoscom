import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pickle
import numpy as np
import sklearn

def app():

    st.markdown('<h1 style="font-size: 40px; text-align: justify;">PROPERTY PRICE PREDICTOR</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 20px; text-align: justify;">La Caculadora del precio de mercado de la vivienda, escoja en el menu de la izquierda las características de su vivienda.</h1>', unsafe_allow_html=True)
    
    st_lottie(requests.get("https://lottie.host/ecc8a4d4-40c8-44ce-933f-1ca4c3041220/0XipcxeEJL.json").json(), height=250, key="Into1")
    
    #st.write('<div style="text-align: justify;"> Escoge las características de tu vivienda en Madrid para obtener un precio .</div>', unsafe_allow_html=True)  

    #Elección de cuidad
    Cuidad=st.sidebar.selectbox("Elige tu ciudad",["MADRID","A CORUÑA"])

    # Slider de selección m2.
    m_cuad=st.sidebar.slider("Selecciona los metros cuadrados de tu vivienda:", min_value=0, max_value=300, value=75, step=1)    
        
    # Slider de selección habitaciones.
    hab=st.sidebar.slider("Selecciona las habitaciones de tu vivienda:", min_value=0, max_value=5, value=2, step=1)    
        
    # Slider de selección baños.
    baños=st.sidebar.slider("Selecciona los baños de tu vivienda:", min_value=0, max_value=3, value=2, step=1)

    # Slider de selección Conservación.
    Conservacion = ["A Estrenar", "En Buen estado", "A Reformar", "Reformado"]
    est_cons=st.sidebar.selectbox("Selecciona el estado de conservación de la vivienda:", Conservacion)

    # Slider de selección Clasificación.
    Clasificacion= ['En trámite','No indicado','Disponible','Pendiente de completar','Exento']
    cert=st.sidebar.selectbox("Selecciona si tiene el certificado energético:", Clasificacion)
    

    with open('forest_madrid.pkl', 'rb') as file:
        modelo = pickle.load(file)

    lat=40.5934447
    lng=-4.1453858
    
   
    model=[lat,lng,baños,hab,m_cuad]

    if est_cons == "A Estrenar":
        model.extend([0,0,0])

    elif est_cons == "En Buen estado":
        model.extend([1,0,0])

    elif est_cons == "A Reformar":
        model.extend([0,1,0])

    elif est_cons == "Reformado":
        model.extend([0,0,1])
    else:
        model.extend([0,0,0])

    

    modelu=modelo.predict([model])
    modelu_round2=np.round(modelu, 2)
    

    
    st.markdown(f"<h1 style='text-align: center; font-size: 48px;'> SU VIVENDA TIENE UN VALOR DE MERCADO DE: {modelu_round2[0]}€ </h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()