import pandas as pd

def targetEncoding(df, target, condition):
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