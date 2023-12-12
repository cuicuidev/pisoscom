import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from .util import geo

from config import WORKDIR, PREDICT_ONE

import requests
import os
import json

def app():

    # <DATA>
    df_journal = pd.read_csv(os.path.join(WORKDIR, 'assets/models/journal.csv'))
    df_journal = df_journal[df_journal.stage == 'validation']

    with open(os.path.join(WORKDIR, 'assets/province_mapping.json'), 'r') as file:
        province_translate: dict = json.load(file)
    # </DATA>

    # <SIDEBAR>
    st.sidebar.markdown("---")

    selected_province=st.sidebar.selectbox("Ir a provincia", sorted([x for x in set(province_translate.values()) if x is not None]))

    lat, lng = geo.getCoordinates(selected_province)



    surface = st.sidebar.slider('Superficie construida (m²)', min_value=25, max_value=1_000, value=75, step=5)
    AVG_NET_SURFACE_OVER_TOTAL_SURFACE = 0.8568
    net_surface = surface * AVG_NET_SURFACE_OVER_TOTAL_SURFACE
    st.sidebar.write(f'La superficie útil calculada es de {net_surface} m²')

    bathrooms = st.sidebar.slider('Número de baños', min_value=1, max_value=5, value=1, step=1)
    rooms = st.sidebar.slider('Número de habitaciones', min_value=0, max_value=10, value=2, step=1)
    age = st.sidebar.slider('Antigüedad', min_value=0, max_value=50, value=15, step=5)
    garden = st.sidebar.checkbox('Jardín', value=False)
    elevator = st.sidebar.checkbox('Ascensor', value=True)
    garage = st.sidebar.checkbox('Garaje o plaza de aparcamiento', value=False)

    BUILD_CONDITIONS = ['A reformar', 'Reformado', 'En buen estado', 'A estrenar']
    if age <= 5: 
        build_condition=st.sidebar.selectbox('Selecciona el estado de conservación:', ['A estrenar'])
    else:
        build_condition=st.sidebar.selectbox('Selecciona el estado de conservación:', BUILD_CONDITIONS)

    st.sidebar.write("---")
    drop_outliers = not st.sidebar.checkbox("Tomar en cuenta los outliers para la predicción")

    # </SIDEBAR>

    # <BODY>
    m = folium.Map(location=(lat, lng), zoom_start=8)
    last_clicked = st_folium(m, width=725)['last_clicked']

    if last_clicked:
        lat, lng = last_clicked['lat'], last_clicked['lng']
    
        st.info(f'Las coordenadas elegidas son: {lat = :.6f}, {lng = :.6f}')

    province = geo.getProvince(lat, lng)
    if province == 'Fail':
        st.error('Haz click en una ubicacación perteneciente a España.')
    else:
        st.info(f'La provincia seleccionada es: {province}')

        if st.button("Calcular precio de la vivienda"):
            price = predict(lat, lng, surface, bathrooms, province, rooms, garden, age, net_surface, elevator, garage, build_condition, drop_outliers)
            st.write(price)
    # </BODY>

def predict(
        lat: float, 
        lng:float , 
        surface: float, 
        bathrooms: int, 
        province: str, 
        rooms: int, 
        garden: bool, 
        age: float, 
        net_surface: float, 
        elevator: bool, 
        garage: bool, 
        build_condition: str,

        drop_outliers: bool = True
        ) -> float:
   form = {
	   'lat': lat,
	   'lng': lng,
	   'surface': surface,
	   'bathrooms': bathrooms,
	   'province': province,
	   'rooms': rooms,
	   'garden': garden,
	   'age': age,
	   'useful_surface': net_surface,
	   'elevator': elevator,
	   'garage': garage,
	   'state': build_condition,
	   'drop_outliers': drop_outliers
   }

   response = requests.post(PREDICT_ONE, json=form)
   price = response.json()
   return price
