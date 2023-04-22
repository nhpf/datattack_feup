# Imports
import pandas as pd

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

# We replace the "," with "." to facilitate processing
ocorrencias['Latitude'] = pd.to_numeric(
    ocorrencias['Latitude'].str.replace(',', '.')
)
ocorrencias['Longitude'] = pd.to_numeric(
    ocorrencias['Longitude'].str.replace(',', '.')
)

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