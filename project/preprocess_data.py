import pandas as pd
import numpy as np


def datetime_to_hours_int(x):
    return [i.total_seconds() / 3600 for i in x]


def clean_data(df, remove_false_alarms=True) -> pd.DataFrame:
    print("df initial length: ", len(df))

    data_clean = df[df["Natureza"] != "1"]
    data_clean = data_clean[data_clean["EstadoOcorrencia"] != "2"]
    data_clean = data_clean[data_clean["Distrito"] != "0"]
    data_clean = data_clean[data_clean["Concelho"] != "0"]
    data_clean = data_clean[data_clean["Numero"] != """\t\t\t\t\t\t\t\t"""]
    # data_clean = data_clean[data_clean['EstadoOcorrencia'] != 'Falso Alerta']
    # data_clean = data_clean[data_clean['EstadoOcorrencia'] != 'Falso Alarme']
    data_clean = pd.concat(
        [
            data_clean[data_clean["EstadoOcorrencia"] == "Encerrada"],
            data_clean[data_clean["EstadoOcorrencia"] == "Falso Alarme"],
        ]
    )

    # We replace the "," with "." to facilitate processing
    data_clean["Latitude"] = pd.to_numeric(data_clean["Latitude"].str.replace(",", "."))
    data_clean["Longitude"] = pd.to_numeric(
        data_clean["Longitude"].str.replace(",", ".")
    )

    print(data_clean["Longitude"][0], " :", type(data_clean["Longitude"][0]))
    print(data_clean["Latitude"][0], " :", type(data_clean["Latitude"][0]))

    data_clean["DataOcorrencia"] = pd.to_datetime(
        data_clean["DataOcorrencia"], format="%d/%m/%Y %H:%M:%S"
    )
    data_clean["DataFechoOperacional"] = pd.to_datetime(
        data_clean["DataFechoOperacional"], format="%d/%m/%Y %H:%M:%S"
    )

    print(data_clean["DataOcorrencia"][0], " :", type(data_clean["DataOcorrencia"][0]))
    print(
        data_clean["DataFechoOperacional"][0],
        " :",
        type(data_clean["DataFechoOperacional"][0]),
    )

    if remove_false_alarms == True:
        data_clean = data_clean[data_clean["EstadoOcorrencia"] != "Falso Alarme"]

    data_clean.dropna(inplace=True)
    print("df length: ", len(data_clean))

    data_clean["hh"] = np.multiply(
        (
            data_clean["NumeroOperacionaisAereosEnvolvidos"]
            + data_clean["NumeroOperacionaisTerrestresEnvolvidos"]
        ),
        datetime_to_hours_int(
            data_clean["DataFechoOperacional"] - data_clean["DataOcorrencia"]
        ),
    )

    return data_clean

    # Define a function to extract category from a string


def _extract_category(string, cat_index):
    if string == "nan" or any(str.isdigit(c) for c in string):
        return
    else:
        parts = string.split("/", 4)
        return parts[cat_index - 1].strip()


# Reformulate categories based on functions defined
def parse_categories(data_clean: pd.DataFrame):
    data_clean["category1"] = (
        data_clean["Natureza"]
        .astype(str)
        .apply(lambda x: _extract_category(x, cat_index=1))
    )
    data_clean["category2"] = (
        data_clean["Natureza"]
        .astype(str)
        .apply(lambda x: _extract_category(x, cat_index=2))
    )
    data_clean["category3"] = (
        data_clean["Natureza"]
        .astype(str)
        .apply(lambda x: _extract_category(x, cat_index=3))
    )

    # Consolidate categories with little statistical relevance
    relevance_threshold = 100
    category_counts = data_clean["category3"].value_counts()
    filtered_categories = category_counts[
        category_counts <= relevance_threshold
    ].index.tolist()
    # Replace the filtered categories with a new "Other" category
    data_clean["category3"] = data_clean["category3"].replace(
        to_replace=filtered_categories, value="Outras ocorrências"
    )

    return data_clean
