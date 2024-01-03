import os

PAGE_CONFIG = {
    "page_title": "Property Price Predictor",
    "page_icon": ":house:",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'mailto:dmitryryzhenkov@cuicui.dev?subject=Property Price Predictor Help',
        'Report a bug': "https://github.com/cuicuidev/pisoscom/issues/new/choose",
        'About': "# About\n\nThis app is a demo of a machine learning model that predicts the price of a property in Spain.\n\nThe model is trained on data from [pisos.com](https://www.pisos.com/).\n\nThe source code is available on [GitHub](https://github.com/cuicuidev/pisoscom).\n\n---\n\nMade by [Dmitry Ryzhenkov](https://cuicui.dev/), [Miguel Nieto Paredes](https://www.linkedin.com/in/miguel-nieto-p) and [Jose Daniel Lema Martinez](https://www.linkedin.com/in/jose-daniel-lema-martinez)." 
    }
}

WORKDIR = __file__[:-9]

PREDICT_ONE = os.environ.get('PREDICT_ONE')

if PREDICT_ONE is None:
    try:
        with open('.env') as file:
            env = file.readlines()

        for line in env:
            key, value = line.split('=')
            if key == 'PREDICT_ONE':
                PREDICT_ONE = value.strip()
                break
    except:
        pass

USE_API = os.environ.get('USE_API')

if USE_API is None:
    try:
        with open('.env') as file:
            env = file.readlines()

        for line in env:
            key, value = line.split('=')
            if key == 'USE_API':
                USE_API = value.strip()
                break
    except:
        pass
