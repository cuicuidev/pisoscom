#Importamos librarias necesarias.
import streamlit as st
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
import pandas as pd

def eda1():
        
        st.title('EDA')

#Cargamos la función con los parametros necesarios que serían los dataframes
# def eda1(df_demanda_nacional,
#         df_demanda_comunidades,
#         df_precios,
#         df_emis_plt,
#         df_gen_plt_eda):
    
#     st.markdown('<h1 style="font-size: 40px; text-align: justify;">ANALISIS EXPLORATORIO DE LOS DATOS</h1>', unsafe_allow_html=True)

#     # Texto Sobre los distintos análisis exploratorios de los datos.
#     st.write('<div style="text-align: justify;"> A continuación, puedes escoger entre los distintos análisis exploratorios\
#               de datos: generación de energía a nivel nacional, emisiones, demanda o precio de la energía.\
#                 </div>', unsafe_allow_html=True)

#     # Animación lottie
#     st_lottie(requests.get("https://lottie.host/c16d2351-863a-48a7-b143-735071d01f92/JQ2hcUD9HM.json").json(), height=250, key="model")

#     # st.selectbox.header('Menú Modelos')
#     opcion = st.selectbox('Seleccione una opción', ['GENERACIÓN', 'EMISIONES', 'DEMANDA','PRECIOS'])

#     ################################################## GENERACIÓN ############################################################## 

#     if opcion == 'GENERACIÓN':
#         st.title('EDA GENERACIÓN')
        
#         # Preparamos los Filtros
#         renovables = ['Hidráulica','Hidroeólica',
#                         'Solar fotovoltaica',
#                         'Solar térmica',
#                         'Otras renovables',
#                         'Eólica',]
        
#         #Creamos los filtros para filtrar por año y por renovable o no renovable.
#         with st.expander('Filtros'):
#                 selected = st.multiselect(label = 'Tipo de energía',
#                     options = ['Renovables', 'No renovables'],
#                     default = ['Renovables','No renovables'],
#                     key = 'generación'
#                     )
        
#                 from_ = st.slider('Desde', 2014, 2022, 2014, key = 'generación_from')
#                 to = st.slider('Hasta', from_, 2022, 2022, key = 'generación_to')

#         columns_gen = [x for x in df_gen_plt_eda.columns if 'Generación' in x]

#         empty = False

#         if len(selected) == 2:
#                 columns = [x for x in columns_gen] + ['Años']
#         elif len(selected) == 0:
#                 empty = True
#         elif selected[0] == 'Renovables':
#                 columns = [x for x in columns_gen if x[11:-4] in renovables] + ['Años']
#         elif selected[0] == 'No renovables':
#                 columns = [x for x in columns_gen if x[11:-4] not in renovables] + ['Años']

#         if not empty:

#                 generacion = df_gen_plt_eda[columns]
#                 generacion = generacion[generacion['Años'].between(from_, to)]
                
#                 #Plot generación por tecnologias barras.
#                 fig=px.bar(data_frame = generacion,
#                 x          = "Años",
#                 y          = generacion.columns[:],
#                 title      ="Evolución de la generación energética por tecnología, Gráfico de barras"
#                 )

#                 fig.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")

#                 st.plotly_chart(figure_or_data = fig, use_container_width = True)
        
        
#                 #Plot generación por tecnologias Lineal.
#                 fig2=px.line(data_frame = generacion,
#                         x = "Años",
#                         y = generacion.columns[:],
#                         title = "Evolución de la generación energética por tecnología")
#                 fig2.update_layout(xaxis_title = "Fecha", yaxis_title = "Gw/h")
#                 st.plotly_chart(fig2)
        
#         st.write('<div style="text-align: justify;"> La generación total no ha sufrido grandes cambios a lo largo de los años, aunque se \
#         aprecia esa pequeña bajada en el año 2020 debido a la pandemia y su posterior\
#         repunte.\
#         Centrándonos en las diferentes tecnologías se puede llegar a las siguientes conclusiones: \
#         Las energías eólica y nuclear se muestran bastante estables a lo largo de los años,\
#         siendo de los pilares más importantes a la hora de la obtención de energía.\
#         En su caso, la gran presencia de la energía eólica se debe al establecimiento de un marco regulatorio\
#         que se ha mantenido estable y a la mejora de la propia tecnología, reduciendo las inversiones\
#         iniciales, los costes de mantenimiento y los costes de explotación, aumentando también la\
#         construcción de numerosos parques eólicos.\
#         Por otro lado, cabe destacar el crecimiento de las centrales de ciclo combinado en detrimento de las centrales de carbón,\
#         esto se debe a que el ciclo combinado es la tecnología mas limpia (menos emisiones de CO2) de las no renovables. \
#         \
#            </div>', unsafe_allow_html=True)


#     ################################################## EMISIONES ##############################################################    
    
#     if opcion == 'EMISIONES':
#         st.title('EDA EMISIONES')

        

#         fig3=px.bar(data_frame = df_emis_plt,
#                     x          = "Años",
#                     y          = df_emis_plt.columns[1:-2],
#                     title = "Emisiones de CO2")
        
#         fig3.update_layout(xaxis_title = "Fecha", yaxis_title = "tCO2 eq./Mwh")
#         st.plotly_chart(figure_or_data = fig3, use_container_width = True)


#         fig4=px.line(data_frame = df_emis_plt,
#                 x = "Años",
#                 y = "tCO2 eq./MWh",
#                 title = "Relación entre emisiones de CO2 y energía generada")


#         st.plotly_chart(figure_or_data = fig4, use_container_width = True)

        

#         st.write('<div style="text-align: justify;"> Observamos como las emisiones de CO2 descienden sobre todo a partir del año 2019 \
#                 produciendose una gran reducción de emisiones entre este año y el 2021, donde se produce un pequeño repunte \
#                 debido a la gerra de Ucrania y las repercusiones de esta sobre el mercado energético.\
#                 A partir de la representación de las emisiones de CO2 de las diferentes tecnologías, se pueden sacar principalmente 2 conclusiones: \
#                     El aumento en la generación energética a partir de las centrales de ciclo combinado, hace que esta tecnología se sitúe entre las más contaminantes pese a ser la energía no renovable más limpia y por otro lado, el repunte después de muchos años de descensos del uso del Carbón como fuente de energía.\
#            </div>', unsafe_allow_html=True)

#     ################################################## DEMANDA ##############################################################
#     if opcion == 'DEMANDA':
#         st.title('EDA DEMANDA')
#         df_demanda_nacional = df_demanda_nacional.drop(columns=["Unnamed: 0"])
#         df_demanda_nacional["Fecha"]=df_demanda_nacional["Fecha"].apply(lambda x : x.split("-")[0])
#         df_demanda_nacional["Fecha"]=df_demanda_nacional["Fecha"].apply(lambda x : int(x))
#         df_demanda_nacional=df_demanda_nacional.groupby("Fecha")['Energia Consumida Mw/h'].sum()
#         df_demanda_nacional=pd.DataFrame(df_demanda_nacional)


        
#         from_ = st.slider('Desde', 2014, 2022, 2014, key = 'generación_from')
#         to = st.slider('Hasta', from_, 2022, 2022, key = 'generación_to')

#         generacion = df_demanda_nacional
#         generacion = generacion.reset_index()
#         generacion = generacion[generacion["Fecha"].between(from_, to)]

#         fig5=px.bar(data_frame = generacion,
#                 x          = "Fecha",
#                 y          = generacion.columns[1:],
#                 title      ="")
#         fig5.update_layout(xaxis_title = "Fecha", yaxis_title = "Mw/h")
#         st.plotly_chart(figure_or_data = fig5, use_container_width = True)

#         st.write('Esta figura representa la demanda nacional anual en Megawatios/h durante los ultimos 11 años. \
#                 Después de una mínima tendencia creciente hasta 2018, observamos en este año un punto de inflexión para continuar con una reducción de la misma en años posteriores.')

        
        
#         X1=df_demanda_comunidades.sum()[2:].sort_values(ascending=False)
               
#         #X1=X1.sort_values   #¿¿¿Como ordeno esto???
#         #st.write(df_demanda_comunidades.sum()[2:].sort_values(ascending=False))
#         fig6= px.bar(x=X1.index,
#                       y=X1, 
#                       title='Demanda electrica por comunidades')
#         fig6.update_layout(xaxis_title = "Comunidades Autónomas", yaxis_title = "Mw/h")
#         st.plotly_chart(fig6)

#         st.write('Observamos que la demanda eléctrica en las distintas comunidades está muy relacionada con la población, \
#                 las comunidades mas pobladas son las que mas energía demandan. (EJ: Andalucía, Cataluña y Madrid.) ')

#     ################################################## PRECIOS ##############################################################    
#     if opcion == 'PRECIOS':
#         st.title('EDA PRECIOS')

        
        
#         # Graficamos la serie temporal de precios
#         fig7 = px.line(df_precios, x = 'Meses',
#                         y = '€/Mwh',
#                           title="Precios en €/Mwh") 
#         st.plotly_chart(fig7)

        
    

if __name__ == "__eda1__":
    eda1()