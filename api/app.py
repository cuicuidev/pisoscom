from fastapi import FastAPI
from config import MODEL_V
import datetime
from pydantic import BaseModel
from enum import Enum
import glob
import pickle as pkl

class StateEnum(str, Enum):
    a_reformar = ' A reformar'
    reformado = ' Reformado'
    a_estrenar = ' A estrenar'
    en_buen_estado = ' En buen estado'

class RequestForm(BaseModel):
    lat: float
    lng: float
    surface: float
    bathrooms: int
    province: str
    rooms: int
    garden: bool
    age: float
    useful_surface: float
    elevator: bool
    garage: bool
    state: StateEnum

    drop_outliers: bool

class Prediction(BaseModel):
    price: float
    # r2_score: float
    # mae: float
    # mse: float
    # val_r2_score: float
    # val_mae: float
    # val_mse: float

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

@app.post('/predict')
async def post_predict(request_form: RequestForm) -> Prediction:
    data = request_form.model_dump()
    print(data)
    prediction = predict(data)
    return prediction