# clean data and count length
import pandas as pd

def clean_data(df, remove_false_alarms=True) -> pd.DataFrame:
    print('df initial length: ', len(df))

    data_clean = df[df['Natureza'] != '1']
    data_clean = data_clean[data_clean['EstadoOcorrencia'] != '2']
    data_clean = data_clean[data_clean['Distrito'] != '0']
    data_clean = data_clean[data_clean['Concelho'] != '0']
    data_clean = data_clean[data_clean['Numero'] != """\t\t\t\t\t\t\t\t"""]
    # data_clean = data_clean[data_clean['EstadoOcorrencia'] != 'Falso Alerta']
    # data_clean = data_clean[data_clean['EstadoOcorrencia'] != 'Falso Alarme']
    data_clean = pd.concat([data_clean[data_clean['EstadoOcorrencia'] == 'Encerrada'], data_clean[data_clean['EstadoOcorrencia'] == 'Falso Alarme']])

    # We replace the "," with "." to facilitate processing
    data_clean['Latitude'] = pd.to_numeric(
        data_clean['Latitude'].str.replace(',', '.')
    )
    data_clean['Longitude'] = pd.to_numeric(
        data_clean['Longitude'].str.replace(',', '.')
    )    

    print(data_clean['Longitude'][0], ' :', type(data_clean['Longitude'][0]))
    print(data_clean['Latitude'][0], ' :', type(data_clean['Latitude'][0]))

    data_clean['DataOcorrencia'] = pd.to_datetime(data_clean['DataOcorrencia'], format='%d/%m/%Y %H:%M:%S').dt.date
    data_clean['DataFechoOperacional'] = pd.to_datetime(data_clean['DataFechoOperacional'], format='%d/%m/%Y %H:%M:%S').dt.date

    print(data_clean['DataOcorrencia'][0], ' :', type(data_clean['DataOcorrencia'][0]))
    print(data_clean['DataFechoOperacional'][0], ' :', type(data_clean['DataFechoOperacional'][0]))

    if remove_false_alarms == True:
        data_clean = data_clean[data_clean['EstadoOcorrencia'] != 'Falso Alarme']

    print('df length: ', len(data_clean))

    return data_clean