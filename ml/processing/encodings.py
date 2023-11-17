import pandas as pd

def targetEncoding(df: pd.DataFrame, target: pd.Series, condition: str) -> tuple:
    """
    Recibe un DataFrame categórico df, una Serie target y una string condition.
    Retorna df con las categorías cambiadas a la mediana o el promedio de la serie target, dependiendo de condition.
    """
    df_target = df.copy()
    df = pd.concat([df_target, pd.DataFrame(target)], axis = 1)
    encodings_map = {}

    for column in df_target.columns:
        if condition == 'target_mean':
            encode = df.groupby(column).mean()[target.name]
            df_target[column] = df_target[column].replace(encode)
            encodings_map[column] = encode
        if condition == 'target_median':
            encode = df.groupby(column).median()[target.name]
            df_target[column] = df_target[column].replace(encode)
            encodings_map[column] = encode
            
    return df_target, encodings_map

def frequencyEncoding(df: pd.DataFrame):
    """
    Recibe un DataFrame categórico df.
    Retorna df con las categorías cambiadas a la frecuencia con la que aparecen.
    """
    df_frequency = df.copy()
    
    encodings_map = {}

    for column in df_frequency.columns:
        encode = df_frequency[column].value_counts()
        df_frequency[column] = df_frequency[column].replace(encode)
        encodings_map[column] = encode
    return df_frequency, encodings_map

def outliersFilter(df: pd.DataFrame, min_price: float, max_price: float, max_baths: float, max_surface: float):
    """
    Recibe un DataFrame df, los máximos y mínimos de price, el máximo de bathrooms y el máximo de surface.
    Retorna df con los outliers filtrados de acuerdo a los parámetros indicados.
    """
    df = df[df['price'].between(min_price, max_price)]
    df = df[df['bathrooms']<=max_baths]
    df = df[df['surface']<=max_surface]
    return df

def binaryEncoding(df: pd.DataFrame):
    """
    Recibe un DataFrame df.
    Retorna df con las catergorías cambiadas a binario.
    """
    df['garage'] = df['garage'].apply(lambda x: 1 if x == 'yes' else 0)
    df['lift'] = df['lift'].apply(lambda x: 1 if x == 'yes' else 0)
    df['garden'] = df['garden'].apply(lambda x: 1 if x == 'yes' else 0)
    df['publisher'] = df['publisher'].apply(lambda x: 1 if x == 'inmobiliaria' else 0)
    return df

def getSample(df: pd.DataFrame, perc: float):
    """
    Recibe un DataFrame 'df' y un porcentaje 'perc'.
    Retorna un DataFrame df_sample para validación.
    """
    df_sample = pd.DataFrame(columns = df.columns)
    for province in df['province'].unique():
        df_prov_sample = df[df['province'] == province]
        if len(df_prov_sample) < 2:
            continue
        df_prov_sample = df_prov_sample.sample(round(df_prov_sample.shape[0]*perc), random_state=42)
        df_sample = pd.concat([df_sample, df_prov_sample], axis=0)
    return df_sample