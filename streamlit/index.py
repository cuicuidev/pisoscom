import streamlit as st
from config import PAGE_CONFIG
from routes import ROUTES

def main():

    st.set_page_config(**PAGE_CONFIG)


    route = st.sidebar.selectbox(label = "Menu", options = list(ROUTES.keys()), index = 0)
    ROUTES[route]()

if __name__ == "__main__":
    main()