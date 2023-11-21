from fastapi import FastAPI
from config import MODEL_V
import datetime
from pydantic import BaseModel
from enum import Enum
import glob
import pickle as pkl

class StateEnum(str, Enum):
    a_reformar = 'A reformar'
    reformado = 'Reformado'
    a_estrenar = 'A estrenar'
    en_buen_estado = 'En buen estado'

class ProvinceEnum(str, Enum):
    a_coruna = 'A Coruña'
    alacant = 'Alacant'
    albacete = 'Albacete'
    almeria = 'Almería'
    araba = 'Araba'
    asturias = 'Asturias'
    badajoz = 'Badajoz'
    barcelona = 'Barcelona'
    bizkaia = 'Bizkaia'
    cantabria = 'Cantabria'
    castello = 'Castelló'
    ceuta = 'Ceuta'
    ciudad_real = 'Ciudad Real'
    cuenca = 'Cuenca'
    caceres = 'Cáceres'
    cadiz = 'Cádiz'
    cordoba = 'Córdoba'
    gipuzcoa = 'Gipuzcoa'
    girona = 'Girona'
    granada = 'Granada'
    guadalajara = 'Guadalajara'
    huelva = 'Huelva'
    huesca = 'Huesca'
    illes_balears = 'Illes Balears'
    jaen = 'Jaén'
    la_rioja = 'La Rioja'
    las_palmas = 'Las Palmas'
    leon = 'León'
    lleida = 'Lleida'
    lugo = 'Lugo'
    madrid = 'Madrid'
    melilla = 'Melilla'
    murcia = 'Murcia'
    malaga = 'Málaga'
    navarra = 'Navarra'
    ourense = 'Ourense'
    palencia = 'Palencia'
    pontevedra = 'Pontevedra'
    salamanca = 'Salamanca'
    santa_cruz_de_tenerife = 'Santa Cruz de Tenerife'
    segovia = 'Segovia'
    sevilla = 'Sevilla'
    soria = 'Soria'
    tarragona = 'Tarragona'
    teruel = 'Teruel'
    toledo = 'Toledo'
    valladolid = 'Valladolid'
    valencia = 'València'
    zamora = 'Zamora'
    zaragoza = 'Zaragoza'
    avila = 'Ávila'

class RequestForm(BaseModel):
    lat: float
    lng: float
    surface: float
    bathrooms: int
    province: ProvinceEnum
    rooms: int
    garden: bool
    age: float
    useful_surface: float
    elevator: bool
    garage: bool
    state: StateEnum

    drop_outliers: bool

class RequestFormMany(BaseModel):
    data: list[RequestForm]

class Prediction(BaseModel):
    price: float
    # r2_score: float
    # mae: float
    # mse: float
    # val_r2_score: float
    # val_mae: float
    # val_mse: float

class PredictionMany(BaseModel):
    predictions: list[Prediction]

app = FastAPI()

def get_paths(province: str, drop_outliers: bool = True) -> tuple[str | bool]:
    m_30 = False
    paths = glob.glob('./models/*.pkl')
    paths = [path for path in paths if province in path]
    if len(paths) == 0:
        path = './models/model_30.pkl'
        path_no_outliers = './models/model_30_no_outliers.pkl'

        encodings = './models/model_30_encodings.pkl'
        encodings_no_outliers = './models/model_30_no_outliers_encodings.pkl'
        m_30=True
    else:
        path = [path for path in paths if 'encodings' not in path and 'outliers' not in path][0]
        path_no_outliers = [path for path in paths if 'encodings' not in path and 'outliers' in path][0]

        encodings = [path for path in paths if 'encodings' in path and 'outliers' not in path][0]
        encodings_no_outliers = [path for path in paths if 'encodings' in path and 'outliers' in path][0]

    if drop_outliers:
        return path_no_outliers, encodings_no_outliers, m_30
    else:
        return path, encodings, m_30
    
def load(path: str):
    with open(path, 'br') as file:
        content = pkl.load(file)
    return content

def predict(data: dict) -> Prediction:
    province = data.get('province')
    drop_outliers = data.get('drop_outliers')
    model_path, encodings_path, m_30 = get_paths(province, drop_outliers)

    model = load(model_path)
    encodings = load(encodings_path)

    if m_30:
        del data['drop_outliers']

        data['province'] = encodings['province'][data['province']]
        data['state'] = encodings['state'].to_dict()[' ' + data['state']]

        price = model.predict([list(data.values())])
    else:
        del data['drop_outliers']
        del data['province']

        data['state'] = encodings['state'].to_dict()[' ' + data['state']]

        price = model.predict([list(data.values())])

    prediction = Prediction(price=price[0])

    return prediction

    
@app.get('/')
async def root() -> dict:
    return {'Status': 'running',
            'Model Version' : MODEL_V,
            'Timestamp' : datetime.datetime.now().timestamp()
            }

@app.post('/predict_one')
async def post_predict_one(request_form: RequestForm) -> Prediction:
    data = request_form.model_dump()
    prediction = predict(data)
    return prediction

@app.post('/predict_many')
async def post_predict_many(request_form_many: RequestFormMany) -> PredictionMany:
    data = request_form_many.model_dump()
    predictions = PredictionMany(predictions=[predict(form) for form in data['data']])
    return predictions

# @app.post('/evaluate')
# async def post_evaluate(request_form_eval: RequestFormEval) -> Eval:
#     data = request_form_eval.model_dump()
#     predictions = [predict(form) for form in data['data']['X']]
#     metrics = get_metrics(predictions, data['data']['y'])
#     e = Eval(metrics)
#     return e