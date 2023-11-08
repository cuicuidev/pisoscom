from bs4 import BeautifulSoup
import glob

def run(args):
    all_endpoints = ['a_coruna', 'alava_araba', 'albacete', 'alicante', 'almeria', 'andorra', 'asturias', 'avila', 'badajoz', 'islas_baleares_illes_balears', 'barcelona', 'bilbao', 'vizcaya_bizkaia', 'burgos', 'caceres', 'cadiz', 'cantabria', 'castellon_castello', 'pisos-cerdanya_francesa', 'pisos-ceuta', 'ciudad_real', 'cordoba', 'cuenca', 'san_sebastian_donostia', 'isla_de_ibiza_eivissa', 'pisos-el_hierro', 'pisos-formentera', 'fuerteventura', 'vitoria_gasteiz_zona_urbana', 'gijon_concejo_xixon_conceyu_gijon', 'guipuzcoa_gipuzkoa', 'girona', 'gran_canaria', 'granada', 'guadalajara', 'guipuzcoa_gipuzkoa', 'huelva', 'huesca', 'isla_de_ibiza_eivissa', 'pisos-pais_vasco_frances_iparralde', 'pamplona_iruna', 'islas_baleares_illes_balears', 'jaen', 'a_coruna', 'la_palma', 'la_rioja', 'lanzarote', 'las_palmas', 'las_palmas_de_gran_canaria', 'leon', 'lleida', 'logrono', 'lugo', 'madrid', 'malaga', 'isla_de_mallorca', 'pisos-melilla', 'isla_de_menorca', 'murcia', 'navarra_nafarroa', 'ourense', 'oviedo', 'pisos-pais_vasco_frances_iparralde', 'palencia', 'isla_de_mallorca_palma_de_mallorca', 'pamplona_iruna', 'pontevedra', 'salamanca', 'san_sebastian_donostia', 'santa_cruz_de_tenerife', 'santander', 'segovia', 'sevilla', 'soria', 'tarragona', 'tenerife', 'teruel', 'toledo', 'valencia', 'valladolid', 'vigo', 'vitoria_gasteiz_zona_urbana', 'vizcaya_bizkaia', 'zamora', 'zaragoza']

    scraped_endpoints = glob.glob('./scraping/data/*.csv')

    scraped_endpoints = [x[:-4].split('\\')[-1] for x in scraped_endpoints]

    remaining_endpoints = [x for x in all_endpoints if x not in scraped_endpoints]

    remaining_endpoints = [x for x in remaining_endpoints if 'pisos-' not in x]

    for endpoint in remaining_endpoints:
        print(endpoint)