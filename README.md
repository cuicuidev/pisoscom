# Calculadora de precios de viviendas

Este repositorio contiene el código de la recolección de datos, del entrenamiento de un modelo de regresión y de interfaces gráfica y API para el modelo en cuestión. Los datos fueron recolectados mediante técnicas de web scraping de manera automatizada gracias al motor de Selenium. Se entrenaron varios modelos Random Forest para el cálculo del precio de los inmuebles. Estos modelos están disponibles en la web como una [app de Streamlit](https://property-price-calculator.streamlit.app). También proporcionamos una imágen de una API estilo REST que pueden desplegar en su servidor para usar el modelo en un entorno de producción.

Navegación:
- api: API estilo REST que unifica nuestros modelos en uno único.
- ml: código de procesado de datos y entrenamiento de los modelos
- scraping: aplicación cli para scrapear cómodamente los endpoints de nuestro _data source_
- streamlit: app de Streamlit desplegada accesible a través de https://property-price-calculator.streamlit.app