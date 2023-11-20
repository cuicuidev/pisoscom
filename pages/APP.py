import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pickle as pkl
import numpy as np
import pandas as pd
import glob

def app():

    st.markdown('<h1 style="font-size: 40px; text-align: justify;">PROPERTY PRICE PREDICTOR</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 20px; text-align: justify;">La Caculadora del precio de mercado de la vivienda, escoja en el menu de la izquierda las características de su vivienda.</h1>', unsafe_allow_html=True)
    
    st_lottie(requests.get("https://lottie.host/ecc8a4d4-40c8-44ce-933f-1ca4c3041220/0XipcxeEJL.json").json(), height=250, key="Into1")
    
    #st.write('<div style="text-align: justify;"> Escoge las características de tu vivienda en Madrid para obtener un precio .</div>', unsafe_allow_html=True)  


    df_provincias=pd.read_parquet('ml/processed_data/tatarabuela.parquet')
    lista_provincias=list(df_provincias.province.unique())


    #Elección de cuidad
    province=st.sidebar.selectbox("Elige tu ciudad",lista_provincias) #Lista de cidades en prceso

    # Slider de selección m2.
    surface=st.sidebar.slider("Selecciona los metros cuadrados de tu vivienda:", min_value=0, max_value=300, value=75, step=1)    
        
    # Slider de selección habitaciones.
    hab=st.sidebar.slider("Selecciona las habitaciones de tu vivienda:", min_value=0, max_value=5, value=2, step=1)    
        
    # Slider de selección baños.
    bathrooms=st.sidebar.slider("Selecciona los baños de tu vivienda:", min_value=0, max_value=3, value=2, step=1)

    # Slider de selección Conservación.
    state = ["A Estrenar", "En Buen estado", "A Reformar", "Reformado"]
    est_cons=st.sidebar.selectbox("Selecciona el estado de conservación de la vivienda:", Conservacion)

    # Slider de selección Clasificación.
    Clasificacion= ['En trámite','No indicado','Disponible','Pendiente de completar','Exento']
    cert=st.sidebar.selectbox("Selecciona si tiene el certificado energético:", Clasificacion)

    # Slider de selección Clasificación.
    lat=st.number_input('Introduce Latitud', min_value=0.00, max_value=100.00, value=40.31, step=0.01)
    lng=st.number_input('Introduce Longitud', min_value=0.00, max_value=100.00, value=48.54, step=0.01)

    #cert=st.sidebar.selectbox("Selecciona si tiene el certificado energético:", Clasificacion)
    

    m_25 = False
    #province = request_form.province

    model_paths = glob.glob("ml/models/*.pkl")
    model_path = [path for path in model_paths if Cuidad in path]

    if len(model_path) == 0:
        model_path = 'ml/models/model_25.pkl'
        m_25=True
    else:
        model_path = model_path[0]
    
    with open(model_path, 'br') as file:
        model = pkl.load(file)

    del file

    # with open('model_test.pkl', 'rb') as file:
    #     modelo = pickle.load(file)

    # lat=40.5934447
    # lng=-4.1453858


    if state == "A Estrenar":
        model.extend([0,0,0])
    elif state == "En Buen estado":
        model.extend([1,0,0])

    elif state == "A Reformar":
        model.extend([0,1,0])

    elif state == "Reformado":
        model.extend([0,0,1])
    else:
        model.extend([0,0,0])

    
    if m_25:
        model_param=[price, lat, lng, surface, bathrooms, province, rooms, garden, age, useful_surface, elevator, garage, state]
    else:
        model_param= [price, lat, lng, surface, bathrooms, rooms, garden, age, useful_surface, elevator, garage, state]

    

    

    modelu=model.predict([model_param])
    modelu_round2=np.round(modelu, 2)
    

    
    st.markdown(f"<h1 style='text-align: center; font-size: 48px;'> SU VIVENDA TIENE UN VALOR DE MERCADO DE: {modelu_round2[0]}€ </h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()