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

def frequencyEncoding(df):
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

def outliersFilter(df, min_price, max_price, max_baths, max_surface):
    """
    Recibe un DataFrame df, los máximos y mínimos de price, el máximo de bathrooms y el máximo de surface.
    Retorna df con los outliers filtrados de acuerdo a los parámetros indicados.
    """
    df = df[df['price'].between(min_price, max_price)]
    df = df[df['bathrooms']<=max_baths]
    df = df[df['surface']<=max_surface]
    return df

def binaryEncoding(df):
    """
    Recibe un DataFrame df.
    Retorna df con las catergorías cambiadas a binario.
    """
    df['garage'] = df['garage'].apply(lambda x: 1 if x == 'yes' else 0)
    df['lift'] = df['lift'].apply(lambda x: 1 if x == 'yes' else 0)
    df['garden'] = df['garden'].apply(lambda x: 1 if x == 'yes' else 0)
    df['publisher'] = df['publisher'].apply(lambda x: 1 if x == 'inmobiliaria' else 0)
    return df


