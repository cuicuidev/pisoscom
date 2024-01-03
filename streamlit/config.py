import os

PAGE_CONFIG = {
    "page_title": "Property Price Predictor",
    "page_icon": ":house:",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
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
