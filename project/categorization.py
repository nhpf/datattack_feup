# Imports
import pandas as pd
import matplotlib.pyplot as plt
from clean_data import clean_data, parse_categories
from ocurrence_frequency import ocurrence_frequency
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Read the database .CSV
ocorrencias = pd.read_csv(
    '../Data/anpc-2016.csv', 
    sep = ',', 
    on_bad_lines='skip'
)

ocorrencias = parse_categories(clean_data(ocorrencias))

frequency_list = ocurrence_frequency(ocorrencias,'category2','Distrito',1)
    

