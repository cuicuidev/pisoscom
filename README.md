# Modelo Deep Learning predicción de precios de la vivienda.

Es:
El objeto del siguiente proyecto hacer una APP que nos permita saber el precio de mercado de una vivienda dadas sus caracteristicas.

En:
The aim of the following project is to determine the market price of a house depending on its characteristics.

Para scrapear una pagina (o reanudar tras un fallor)
```sh
python cli.py scrape -e 'endpoint'
```

Para guardar extraer el contenido y guardarlo en csv una vez se ha terminado de scrapear
```sh
python cli.py commit -f 'filename'
```

Para resetear el entorno y poder scrapear de nuevo
```sh
python cli.py reset
```