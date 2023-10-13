import numpy as np

def dropOutliers(df, threshold):
    """
    Recibe un DataFrame numérico data_frame y un float threshold (por defecto = 2.0).
    Retorna data_frame despues de aplicar outliers() a todas las columnas.
    """
    df = df.copy()

    for column in df.columns:
        df = df[df[column].between(outliers(df[column], threshold)[0], outliers(df[column], threshold)[1])]
        
    return df

def outliers(serie, threshold = 1.5):
    """
    Recibe una Serie serie y un float umbral (por defecto = 1.5).
    Retorna los puntos de corte inferior y superior para eliminar outliers.
    """
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    ric = q3 - q1
    
    lower = q1 - threshold * ric
    upper = q3 + threshold * ric
    
    return lower, upper

def getBestOutliersThreshold(df, data_loss, range_ = 100):
    """
    Recibe un DataFrame numérico data_frame, un float loss (por defecto = 0.05) y un int range_ (por defecto = 1_000).
    Retorna int i para como el mejor (elimina outliers sin superar loss) threshold para utilizar en dropOutliers().
    Arroja una excepción en caso de no encontrar el mejor valor i para el range_ establecido.
    """
    df = df.copy()
    
    original = df.shape[0]
    
    for i in np.arange(0, range_, 0.3):
        new_size = dropOutliers(df, i).shape[0]
        if (1 - new_size/original) <= data_loss:
            return i
    
    return i
    raise Exception(f'No thresholds found for floats up to {range_} to meet a minimum of {data_loss} data loss.')