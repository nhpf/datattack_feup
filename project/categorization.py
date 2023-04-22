# Imports
import pandas as pd


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
def extract_category2_3(string):
    parts = string.split("/", 1)
    if len(parts) > 1:
        return parts[1].rsplit("/", 1)[0]
    else:
        return ""

#Verifying the uniqueness of occurence nature labeling

categorias = ocorrencias['Natureza'].unique()

print(categorias)


# Compare length for unique elements
if(len(set(categorias)) == len(categorias)):

   print("All elements are unique.")
else:
   print("All elements are not unique.")

print(len(categorias))

for value in categorias:
    ocorrencias['Natureza']
    

ocorrencias['category2_3'] = ocorrencias['Natureza'].astype(str).apply(extract_category2_3)

# Display the DataFrame with the new "category2_3" column
print(ocorrencias['category2_3'])
# Check the size and shape of the database
#ocorrencias.shape

