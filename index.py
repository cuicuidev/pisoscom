#Importamos las librerias necesarias.
import streamlit as st
from streamlit_lottie import st_lottie  #Libreria necesaria para trabajar con lotties archivos json animados
from streamlit_option_menu import option_menu    #Libreria necesaria para trabajar con lotties archivos json animados
from pages import APP
from pages import Autores

def main():

    st.set_page_config(
    page_title="Property Price Predictor",
    page_icon=":house:"
    )

    # Creamos un MENÚ.
    opcion=st.sidebar.selectbox("Menú", 
                                ["APP",
                                 "AUTORES"])

    if opcion == 'APP':
        APP.app()

    elif opcion == 'AUTORES':  
        Autores.Autores()

if __name__ == "__main__":
    main()