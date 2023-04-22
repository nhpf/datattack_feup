import pandas as pd
import matplotlib.pyplot as plt

population = pd.read_csv('data.csv')
print('csv number of columns: ', len(population.columns))
print(population.columns)
print(population.head())
population.plot(x='Local de residência', y='População residente', kind='bar')
# plt.bar(population['Local de residência'], population['População residente'])
# plt.xticks(rotation=45)
plt.show()