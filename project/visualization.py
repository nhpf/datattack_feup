import pandas as pd
from clean_data import clean_data
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv('../Data/anpc-2016.csv')
print(data.head())

data_clean = clean_data(data)

def general_plots(df):
    print('df.columns: ', df.columns)

general_plots(data_clean)
