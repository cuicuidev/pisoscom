import streamlit as st
from config import WORKDIR
import os

def about():
    st.title('Autores') 
        
    #Establecemos columnas para dar orden a los autores.
    col1, col2 = st.columns([1, 1])
    col3, col4,col5,col6 = st.columns([1, 1, 1, 1])
    col7, col8 , col9= st.columns([1, 1, 1])
    col9, col10,col11,col12, col13, col14 = st.columns([1, 1, 1, 1,1,1]) 
    
    #Autores:
    col1.subheader('DMITRY RYZHENKOV') 
    col1.image(os.path.join(WORKDIR, 'assets/images/dmitry.jpg'),width=150)
    # [<img src="URL_de_la_imagen" width="200" height="100">](URL_del_enlace)

    col3.markdown("[![Linkedin](<https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg>)](<https://www.linkedin.com/in/cuicuidev/>)")   
    col4.markdown("[![GuitHub](<https://img.icons8.com/material-outlined/48/000000/github.png>)](<https://github.com/cuicuidev>)")

    col2.subheader('MIGUEL NIETO') 
    col2.image(os.path.join(WORKDIR, 'assets/images/miguel.jpg'),width=150)   
    col5.markdown("[![Linkedin](<https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg>)](<https://www.linkedin.com/in/miguel-nieto-p/>)")   
    col6.markdown("[![GuitHub](<https://img.icons8.com/material-outlined/48/000000/github.png>)](<https://github.com/MiguelNietoP>)")

    
    col8.subheader('DANIEL LEMA') 
    col8.image(os.path.join(WORKDIR, 'assets/images/daniel_2.jpeg'),width=150)
    col11.markdown("[![Linkedin](<https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg>)](<https://www.linkedin.com/in/jose-daniel-lema-martinez/>)")   
    col12.markdown("[![GuitHub](<https://img.icons8.com/material-outlined/48/000000/github.png>)](<https://github.com/Dande8719?tab=followers>)")