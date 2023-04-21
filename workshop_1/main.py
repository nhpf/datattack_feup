import pandas as pd

river_level_by_hour = pd.read_csv("./data/Pavia-Nivel_do_rio_por_hora.csv")
rain_by_hour = pd.read_csv("./data/Pavia-Quantidade_chuva_por_hora.csv")

print(river_level_by_hour.head())
print(rain_by_hour.head())

rain_by_hour

