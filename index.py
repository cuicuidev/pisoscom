#Importamos las librerias necesarias.
import streamlit as st
from streamlit_lottie import st_lottie  #Libreria necesaria para trabajar con lotties archivos json animados
from streamlit_option_menu import option_menu    #Libreria necesaria para trabajar con lotties archivos json animados

#Importamos funciones de codigo en otros archivos
# from intro import introduccion
# from eda import eda1
# from pages.Autores import Autores
# from pages.APP import app
from pages import APP
from pages import Autores

# Cargamos los DataFrames necesarios para el proyecto. Tengo todos los del EDA.


#df_precios = pd.read_csv("DF/Precios por mes.csv")




#Creamos el marco de trabajo de Streamlit.

def main():

    st.set_page_config(
    page_title="Property Price Predictor",
    page_icon=":house:"
    )

    # Creamos un MENÚ.
    opcion=st.sidebar.selectbox("Menú", 
                                ["APP",
                                 "AUTORES"])
    


    #################################### INTRODUCCÓN ################################################
    #################################################################################################
    #################################################################################################

    if opcion == 'APP':
        APP.app()

        

    #################################### AUTORES ##################################################
    ################################################################################################
    ################################################################################################

    elif opcion == 'AUTORES':  
        Autores.Autores()

    ############################# CARGAMOS IMÁGENES Y PIE  DE PÁGINA #######################
    ###############################################################################################
    ###############################################################################################    

    # st.markdown("***")
    # col1, col2, col3 = st.columns([2, 3, 1])
    #Introcucimos imagenes principales para la página.
    
    
    
    ############################# CERRAMOS ESTRUCTURA DEL MODELO ########################
    ############################################################################################
    ############################################################################################

if __name__ == "__main__":
    main()