import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pickle as pkl
import json
import numpy as np
import pandas as pd
import glob
import streamlit as st
from streamlit_folium import st_folium
import folium
from . import functions

def app():

    st.markdown('<h1 style="font-size: 40px; text-align: justify;">PROPERTY PRICE PREDICTOR</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 20px; text-align: justify;">La Caculadora del precio de mercado de la vivienda. Indica, en el menu de la izquierda, las características de tu vivienda.</h1>', unsafe_allow_html=True)
    
    st_lottie(requests.get("https://lottie.host/ecc8a4d4-40c8-44ce-933f-1ca4c3041220/0XipcxeEJL.json").json(), height=150, key="Into1")
        
    with open('province_translate.json', 'r') as file:
        province_translate = json.load(file)

    selected_province=st.sidebar.selectbox("Provincia a mostrar", sorted([x for x in set(province_translate.values()) if x is not None]))
    
    # lat, lng = 35.782170703266075, -8.041992187500002 # Localiza el centro del mapa que vamos a mostrar
    lat, lng = functions.getCoordinates(selected_province)

    m = folium.Map(location=(lat, lng), zoom_start=8)
    last_clicked = st_folium(m, width=725)['last_clicked']

    if last_clicked:
        lat, lng = last_clicked['lat'], last_clicked['lng']
    
    st.info(f'Las coordenadas elegidas son: {lat = :.6f}, {lng = :.6f}')

    df_provincias = pd.read_parquet('ml/processed_data/tatarabuela.parquet')
    # lista_provincias=list(df_provincias.province.unique())
    df_30 = pd.read_parquet('ml/processed_data/provinces/data_30.parquet')
    states = sorted([x for x in df_30.state.unique() if x is not None])

    df_journal = pd.read_csv('ml/models/journal.csv')
    df_journal = df_journal[df_journal.stage == 'validation']

    del df_provincias
    del df_30
    
    # Slider de selección surface.
    surface = st.sidebar.slider('Selecciona los m² construidos:', min_value=25, max_value=1_000, value=75, step=5)
        
     # Slider de selección bathrooms.
    bathrooms = st.sidebar.slider('Selecciona el número de baños:', min_value=1, max_value=5, value=1, step=1)
    
    # Slider de selección rooms.
    rooms = st.sidebar.slider('Selecciona el número de habitaciones:', min_value=0, max_value=10, value=2, step=1)
    
    # Slider de selección age
    age = st.sidebar.slider('Selecciona el número de años:', min_value=0, max_value=50, value=15, step=5)
    
    # Slider de selección useful_surface
    useful_surface = surface*0.8568
    st.sidebar.write(f'La superficie útil calculada es: {useful_surface}m²')
    
    # Slider de selección garden
    garden = st.sidebar.checkbox('Marca la casilla si tiene jardín', value=False)
    
    # Slider de selección elevator
    elevator = st.sidebar.checkbox('Marca la casilla si tiene ascensor', value=True)
    
    # Slider de selección garage
    garage = st.sidebar.checkbox('Marca la casilla si tiene garaje', value=False)

    # Slider de selección state.
    if age <= 5: # en caso de que queramos cambiar el step de age en el futuro
        state=st.sidebar.selectbox('Selecciona el estado de conservación:', [x for x in states if x == ' A estrenar'])
    else:
        state=st.sidebar.selectbox('Selecciona el estado de conservación:', [x for x in states if x != ' A estrenar'])
        
    # Selección province
    province = functions.getProvince(lat, lng)
    if province == 'Fail':
        st.error('Haz click en una ubicacación perteneciente a España.')
    else:
        st.info(f'La provincia seleccionada es: {province}')
        
        # modelos

        m_30 = False

        model_paths = glob.glob("ml/models/*.pkl")
        model_data = [path for path in model_paths if province.lower() in path.split('\\')[-1].lower()]

        # st.write(model_data)

        if len(model_data) == 0:
            model_path = 'ml/models/model_30.pkl'
            model_path_no_outliers = 'ml/models/model_30_no_outliers.pkl'

            model_encodings = 'ml/models/model_30_encodings.pkl'
            model_encodings_no_outliers = 'ml/models/model_30_no_outliers_encodings.pkl'
            m_30=True
        else:
            model_path = [path for path in model_data if 'encodings' not in path and 'outliers' not in path][0]
            model_path_no_outliers = [path for path in model_data if 'encodings' not in path and 'outliers' in path][0]

            model_encodings = [path for path in model_data if 'encodings' in path and 'outliers' not in path][0]
            model_encodings_no_outliers = [path for path in model_data if 'encodings' in path and 'outliers' in path][0]


        no_outliers = st.checkbox('Marca la casilla si quieres quitar ourliers', value=False)

        model_path = model_path_no_outliers if no_outliers else model_path
        model_encodings = model_encodings_no_outliers if no_outliers else model_encodings

        # st.write(model_path)
        # st.write(model_encodings)

        df_journal = df_journal[df_journal['file'].apply(lambda x: x[4:-8].lower() in model_path.lower())]
        df_journal = df_journal[~df_journal['with_outliers'] if no_outliers else df_journal['with_outliers']]
        
        with st.expander('Más información'):
            st.write(df_journal[df_journal['stage'] == 'validation'])

        with open(model_path, 'rb') as file:
            model = pkl.load(file)

        with open(model_encodings, 'rb') as file:
            encodings = pkl.load(file)
        
        del file
        
        state = encodings['state'][state]

        if not m_30:
            y_test = [[lat, lng, surface, bathrooms, rooms, garden, age, useful_surface, elevator, garage, state]]
        else:
            province = encodings['province'][province]
            y_test = [[lat, lng, surface, bathrooms, province, rooms, garden, age, useful_surface, elevator, garage, state]]

        # Cambiamos la predicción a un formato de número que se lea fácil (miles y millones)
        predict_value = str(round(model.predict(y_test)[0]))
        if len(predict_value) <= 6:
            predict_value = predict_value[:-3] + '.' + predict_value[-3:]
        else:
            predict_value = predict_value[:-6] + '.' + predict_value[-6:-3] + '.' + predict_value[-3:]
        st.success(f'El valor de la vivienda es de: {predict_value}€')
        

if __name__ == "__main__":
    app()





