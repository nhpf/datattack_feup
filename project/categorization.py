# Imports
import pandas as pd
import operator
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
    'Data/anpc-2016.csv', 
    sep = ',', 
    on_bad_lines='skip'
)

ocorrencias = clean_data(ocorrencias)

# Define a function to extract category from a string
def extract_category(string, cat_index):
    # print(string)
    if string == "nan" or any(str.isdigit(c) for c in string):
        return
    else:
        parts = string.split("/", 4)
        return parts[cat_index-1].strip()


#Reformulate categories based on functions defined
ocorrencias['category1'] = ocorrencias['Natureza'].astype(str).apply(lambda x: extract_category(x,cat_index=1))
ocorrencias['category2'] = ocorrencias['Natureza'].astype(str).apply(lambda x: extract_category(x,cat_index=2))
ocorrencias['category3'] = ocorrencias['Natureza'].astype(str).apply(lambda x: extract_category(x,cat_index=3))

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
print(ocorrencias['category1'].value_counts())
print(ocorrencias['category2'].value_counts())
print(ocorrencias['category3'].value_counts())


#Parses the data and makes list of lists based on unique values for the Districts columns
dist_list = []
abreviation_dict = {'Assistência e Prevenção a actividades humanas' : 1, 'Comprometimento total ou parcial de segurança, serviços ou estruturas': 2,
                    'Incêndios Urbanos ou em Área Urbanizável':3, 'Incêndios em Equipamento e Produtos':4}

for row1 in ocorrencias['Distrito'].unique():
    cat2_list = []
    i = 0
    #Parses the Districts columns to count ocurrences
    for row2 in ocorrencias['Distrito']:
        if row1 == row2:
            category = ocorrencias['category2'].iloc[i]
            #Abbreviates some categories for better visualization graphs
            if category in abreviation_dict:
                value = abreviation_dict[category]
                if value == 1:
                    category = "Assist e Prev a actv humanas"
                elif value == 2:
                    category = "Comp total ou parcial de seg"
                elif value == 3:
                    category = "Incêndios urbanos"
                elif value == 4:
                    category = "Incêndio em equipm"
            #Verifies if category is in list and adds to occurrence count if it does, adds category to list if it doesn't
            if category in cat2_list:
                cat2_list.index(category)
                cat2_list[cat2_list.index(category)+1] = cat2_list[cat2_list.index(category)+1] + 1
            else:
                cat2_list.append(category)
                cat2_list.append(1)
        i = i + 1
    dist_list.append(cat2_list)
    


# Transform the elements in each sublist into tuples of two
list_of_tuples = [[(lst[2*i], lst[2*i+1]) for i in range(round(len(lst)/2-1))] for lst in dist_list]

#Define a counter and makes relation between Ocurrences and Districts for visualization of data
j = 0
for row1 in ocorrencias['Distrito'].unique():
    list_of_tuples[j] = sorted(list_of_tuples[j], key = lambda x: (x[0]))
    print(row1,':', list_of_tuples[j], "\n\n\n")
# Separate the x and y values into two lists
    x_values = [x[0] for x in list_of_tuples[j]]
    y_values = [x[1] for x in list_of_tuples[j]]
# Plot the data
    plt.bar(x_values, y_values)
    plt.title("Breakdown of ocurrences for" + " " + str(row1))
    plt.xlabel("Ocurrence type")
    plt.xticks(fontsize=8,rotation=45,ha='right')
    plt.ylabel("Number of ocurrences")
    plt.tight_layout()
    plt.show()
    j = j+1

