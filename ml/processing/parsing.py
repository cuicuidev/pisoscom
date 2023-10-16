import pandas as pd
import numpy as np
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