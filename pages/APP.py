import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pickle as pkl
import numpy as np
import pandas as pd
import glob
import streamlit as st
from streamlit_folium import st_folium
import folium

def app():

    st.markdown('<h1 style="font-size: 40px; text-align: justify;">PROPERTY PRICE PREDICTOR</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 20px; text-align: justify;">La Caculadora del precio de mercado de la vivienda, escoja en el menu de la izquierda las características de su vivienda.</h1>', unsafe_allow_html=True)
    
    st_lottie(requests.get("https://lottie.host/ecc8a4d4-40c8-44ce-933f-1ca4c3041220/0XipcxeEJL.json").json(), height=250, key="Into1")
    
    #st.write('<div style="text-align: justify;"> Escoge las características de tu vivienda en Madrid para obtener un precio .</div>', unsafe_allow_html=True)  

    lat, lng = 35.782170703266075, -8.041992187500002

    m = folium.Map(location=(lat, lng), zoom_start=5)
    last_clicked = st_folium(m, width=725)['last_clicked']

    if last_clicked:
        lat, lng = last_clicked['lat'], last_clicked['lng']

    st.write(f'{lat = :.6f}, {lng = :.6f}')

    df_provincias=pd.read_parquet('ml/processed_data/tatarabuela.parquet')
    lista_provincias=list(df_provincias.province.unique())
    df_25 = pd.read_parquet('ml/processed_data/provinces/data_25.parquet')
    lista_estados = list(df_25.state.unique())

    df_journal = pd.read_csv('ml/models/journal.csv')
    df_journal = df_journal[df_journal.stage == 'validation']

    del df_provincias
    del df_25

    #Elección de cuidad
    province=st.sidebar.selectbox("Elige tu ciudad",lista_provincias) #Lista de cidades en prceso

    # Slider de selección m2.
    m_cuad=st.sidebar.slider("Selecciona los metros cuadrados de tu vivienda:", min_value=0, max_value=300, value=75, step=1)    
        
    # Slider de selección habitaciones.
    hab=st.sidebar.slider("Selecciona las habitaciones de tu vivienda:", min_value=0, max_value=5, value=2, step=1)    
        
    # Slider de selección baños.
    baños=st.sidebar.slider("Selecciona los baños de tu vivienda:", min_value=0, max_value=3, value=2, step=1)

    # Slider de selección Conservación.

    est_cons=st.sidebar.selectbox("Selecciona el estado de conservación de la vivienda:", lista_estados)

    # Slider de selección Clasificación.
    Clasificacion= ['En trámite','No indicado','Disponible','Pendiente de completar','Exento']
    cert=st.sidebar.selectbox("Selecciona si tiene el certificado energético:", Clasificacion)
    

    m_25 = False
    #province = request_form.province

    model_paths = glob.glob("ml/models/*.pkl")
    model_data = [path for path in model_paths if province in path]

    st.write(model_data)

    if len(model_data) == 0:
        model_path = 'ml/models/model_25.pkl'
        model_path_no_outliers = 'ml/models/model_25_no_outliers.pkl'

        model_encodings = 'ml/models/model_25_encodings.pkl'
        model_encodings_no_outliers = 'ml/models/model_25_no_outliers_encodings.pkl'
        m_25=True
    else:
        model_path = [path for path in model_data if 'encodings' not in path and 'outliers' not in path][0]
        model_path_no_outliers = [path for path in model_data if 'encodings' not in path and 'outliers' in path][0]

        model_encodings = [path for path in model_data if 'encodings' in path and 'outliers' not in path][0]
        model_encodings_no_outliers = [path for path in model_data if 'encodings' in path and 'outliers' in path][0]


    no_outliers = st.selectbox('NO OUTLIERS', [True, False])

    model_path = model_path_no_outliers if no_outliers else model_path
    model_encodings = model_encodings_no_outliers if no_outliers else model_encodings

    st.write(model_path)
    st.write(model_encodings)

    df_journal = df_journal[df_journal.file.apply(lambda x: x[4:-8] in model_path)]
    df_journal = df_journal[~df_journal.with_outliers if no_outliers else df_journal.with_outliers]
    st.write(df_journal)

    with open(model_path, 'rb') as file:
        model = pkl.load(file)

    with open(model_encodings, 'rb') as file:
        encodings = pkl.load(file)
    
    del file

    surface = m_cuad
    bathrooms = baños
    rooms = hab
    garden = False
    age = 20
    useful_surface = m_cuad*0.85
    elevator = True
    garage = True
    state = encodings['state'][est_cons]

    if not m_25:
        y_test = [[lat, lng, surface, bathrooms, rooms, garden, age, useful_surface, elevator, garage, state]]
    else:
        province = encodings['province'][province]
        y_test = [[lat, lng, surface, bathrooms, province, rooms, garden, age, useful_surface, elevator, garage, state]]

    st.write(f'Predicción {model.predict(y_test)=}')


    
   
    # model=[lat,lng,baños,hab,m_cuad]

    # if est_cons == "A Estrenar":
    #     model.extend([0,0,0])

    # elif est_cons == "En Buen estado":
    #     model.extend([1,0,0])

    # elif est_cons == "A Reformar":
    #     model.extend([0,1,0])

    # elif est_cons == "Reformado":
    #     model.extend([0,0,1])
    # else:
    #     model.extend([0,0,0])

    

    # modelu=modelo.predict([model])
    # modelu_round2=np.round(modelu, 2)
    

    
    # st.markdown(f"<h1 style='text-align: center; font-size: 48px;'> SU VIVENDA TIENE UN VALOR DE MERCADO DE: {modelu_round2[0]}€ </h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()