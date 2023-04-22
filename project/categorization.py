# Imports
import pandas as pd
import matplotlib.pyplot as plt
from clean_data import clean_data
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Read the database .CSV
ocorrencias = pd.read_csv(
    'https://raw.githubusercontent.com/centraldedados/protecao_civil/master/data/anpc-2016.csv', 
    sep = ',', 
    on_bad_lines='skip'
)

ocorrencias = clean_data(ocorrencias)

# Define a function to extract "category2/category3" from a string
def extract_category3(string):
    #print(string)
    if string == 'nan' or any(str.isdigit(c) for c in string):
        return
    else:
        parts = string.split("/", 4)
        return parts[2].strip()
    
def extract_category2(string):
    #print(string)
    if string == 'nan' or any(str.isdigit(c) for c in string):
        return
    else:
        parts = string.split("/", 4)
        return parts[1].strip()


#Reformulate categories based on functions defined
ocorrencias['category2'] = ocorrencias['Natureza'].astype(str).apply(extract_category2)
ocorrencias['category3'] = ocorrencias['Natureza'].astype(str).apply(extract_category3)

#Print results of level 2 and level 3 nodes of category tree before consolidation
#print(ocorrencias['category2'].value_counts())
#print(ocorrencias['category3'].value_counts())

#Consolidate categories with little statistical relevance
relevance_threshold = 100
category_counts = ocorrencias['category3'].value_counts()
filtered_categories = category_counts[category_counts <= relevance_threshold].index.tolist()
# Replace the filtered categories with a new "Other" category
ocorrencias['category3'] = ocorrencias['category3'].replace(
    to_replace=filtered_categories,
    value='Outras ocorrências'
)

# Display the updated value counts
print(ocorrencias['category2'].value_counts())
print(ocorrencias['category3'].value_counts())

#ocorrencias['category2'] = ocorrencias['category2'].astype(str)
#ocorrencias['category3'] = ocorrencias['category3'].astype(str)
#ocorrencias['Distrito'] = ocorrencias['Distrito'].astype(str)
#ocorrencias['Concelho'] = ocorrencias['Concelho'].astype(str)
#ocorrencias['Freguesia'] = ocorrencias['Freguesia'].astype(str)
#ocorrencias['NumeroMeiosTerrestresEnvolvidos'] = ocorrencias['NumeroMeiosTerrestresEnvolvidos'].astype(int)
#ocorrencias['NumeroOperacionaisTerrestresEnvolvidos'] = ocorrencias['NumeroOperacionaisTerrestresEnvolvidos'].astype(int)
#ocorrencias['NumeroMeiosAereosEnvolvidos'] = ocorrencias['NumeroMeiosAereosEnvolvidos'].astype(int)
#ocorrencias['NumeroOperacionaisAereosEnvolvidos'] = ocorrencias['NumeroOperacionaisAereosEnvolvidos'].astype(int)


#print(ocorrencias['Distrito'].value_counts())


#df_cat2dist = ocorrencias[['category2','Distrito']]

#plt.matshow(df_cat2dist.corr())
#plt.show()

# Convert the string data to numerical labels
#le = LabelEncoder()
#ocorrencias['cat2_le'] = le.fit_transform(ocorrencias['category2'])
#ocorrencias['Distrito_le'] = le.fit_transform(ocorrencias['Distrito'])

# Compute the correlation matrix
#corr = ocorrencias[['cat2_le', 'Distrito_le']].corr()

# Create a heatmap plot
#sns.heatmap(corr, cmap='coolwarm', annot=True)
#plt.show()

# Create a scatter plot
#ocorrencias.plot(kind='scatter', x='Distrito', y='category2')

#Plot grapg
#plt.title('Incident Locations')
#plt.xlabel('Distrito')
#plt.ylabel('Category - Type 2')
#plt.show()
