import pandas as pd
import numpy as np
import ast
import re

##############################################################################################################

def tryInt(n):
    try:
        return int(''.join(n[:-2].split('.')))
    except: return np.nan
    
def tryLiteralEval(row):
    try:
        return ast.literal_eval(row)
    except:
        return lambda _: np.nan

##############################################################################################################

# HAY QUE REFACTORIZAR ESTE CHURRO HORRIBLE!!!!!!!

def freeChurro(df):
    columns = []
    characteristics = df['characteristics'].iloc

    for chars in characteristics:
        for char in chars:
            vals = char.split(':')
            if isinstance(vals, list):
                columns.append(vals[0])
            else:
                columns.append(vals)

    columns = [x.strip() for x in columns]
    columns = list(set(columns))
    data = []

    for chars in characteristics:

        dict_data = {}

        for char in chars:
            content = char.split(':')
            if len(content) == 2:
                key, value = content
                key = key.strip()
                dict_data[key] = value
            else:
                key, value = content[0], content[0]
                key = key.strip()
                dict_data[key] = value

        dict_columns = {}

        for column in columns:
            for key, value in dict_data.items():
                if key == column:
                    dict_columns[column] = value
            
        for column in columns:
            if dict_columns.get(column) is None:
                dict_columns[column] = np.nan

        data.append(dict_columns)
        
    return pd.DataFrame(data)

# HAY QUE REFACTORIZAR ESTE CHURRO HORRIBLE!!!!!!!

##############################################################################################################

def nanPercentage(col):
    orig_size = len(col)
    drop_size = len(col.dropna())
    return 1 - drop_size/orig_size

def nanReport(threshold, df_):
    df = df_[[col for col in df_.columns if nanPercentage(df_[col]) < threshold]]
    print(f'Porcentaje de valores perdidos en total: {1- df.dropna().shape[0] / df.shape[0]}')
    print(f'Columnas conservadas: {len(df.columns)}')
    return df

##############################################################################################################

def getType(df):
    type_ = []
    
    for n in df['title']:
        if pd.isna(n):
            type_.append(np.nan)
            continue
        if len(n) != 1:
            name = n.split()[0]
            type_.append(name)
        else: type_.append(n)
    
    df['type'] = type_
    
    return df

def getStreetType(df):
    
    types = ['calle', 'c', 'avenida', 'avda', 'av', 'plaza', 'pz', 'carretera', 'bulevar', 'boulevard', 'parque', 'paseo', 'autovía', 'autovia']
    patterns = [r'\b(?:' + re.escape(x) + r')\b' for x in types]
    
    street = []
    
    for n in df['location']:
        if pd.isna(n):
            street.append(np.nan)
            continue
        
        matches = []
        
        for pattern in patterns:
            match_ = re.findall(pattern, n.lower())
            if match_ is not None:
                matches.extend(match_)
            else: matches.append(False)
        
        if any(matches):
            street.append(' '.join([x for x in matches]))
        else: street.append(np.nan)
    
    df['street'] = street
    
    return df

# def getStreet(df):
#     street = []
    
#     for n in df['location']:
#         if pd.isna(n):
#             street.append(np.nan)
#             continue
#         if len(n) != 1:
#             name = n.split()[0]
#             street.append(name)
#         else: street.append(n)
    
#     df['street'] = street
    
#     return df

def read_csv(path: str) -> pd.DataFrame:
    with open(path, encoding = 'utf-8') as file:
        data = file.readlines()
        
    pattern_dict = r'\{([^}]+)\}' #patrón para detectar diccionarios
    pattern_list = r'\[([^]]+)\]' #patrón para detectar listas

    df = pd.DataFrame(columns=['price', 'title_location', 'lat', 'lng', 'province', 'last_updated', 'agency', 'characteristics', 'meta_data'])
    
    for row in data[1:]:
        new_row = {}

        match = re.findall(pattern_dict, row) # buscamos cualquier cosa que parezca un diccionario
        if len(match) == 0:
            new_row['meta_data'] = np.nan
            row = row[:- 3]
        else:
            new_row['meta_data'] = ast.literal_eval('{' + match[-1] + '}') # parseamos el diccionario

            row = row[:- 4 -len(match[-1])] # borramos la representación del diccionario de meta_data
        row = row.split(',') # separamos por coma
        
        new_row['last_updated'] = row.pop() # sacamos la columna last_updated
        new_row['agency'] = row.pop() # sacamos la columna agency

        row = ','.join(row) # juntamos con comas

        match = re.findall(pattern_list, row) # buscamos cualquier cosa que parezca una lista

        try:
            if len(match) == 0:
                new_row['characteristics'] = np.nan
            else:
                new_row['characteristics'] = ast.literal_eval('[' + match[-1] + ']') # parseamos la lista
        except:
            new_row['characteristics'] = np.nan

        try:
            row = row[:- 4 -len(match[0])] # borramos la representación de la lista
        except:
            row = row[:-3]

        row = row.split(',') # separamos por coma

        new_row['lng'] = row.pop() # sacamos columna de longutud
        new_row['lat'] = row.pop() # sacamos columna de latitud
        new_row['price'] = row.pop(0) # sacamos la columna de precio

        new_row['title_location'] = ','.join(row) # sacamos titulo y calle (hay comas molestando, no sé como separar bien las dos columnas)
        
        new_row['province'] = path

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

def tryNan(x):
    if pd.isna(x):
        return np.nan
    if 'consultar' in x:
        return np.nan
    
    try:
        return int(''.join(x[:-2].split('.')))
    except:
        return np.nan
    
def tryFloat(x):
    try:
        return float(x)
    except:
        return np.nan